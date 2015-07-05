#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, django, json

# Get config from json
with open('config.json') as config:
    config = json.load(config)
project_dir = config['project_dir']
project_name = config['project_name']
domain = config['domain']
uid = config['uid_start']
gid = config['gid_start']

# Connect to django models
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", project_name + ".settings")
from django.conf import settings
django.setup()
from django.contrib.auth.models import User
from django.db.models.loading import get_model

if 'extended_user_profile' in config:
    app_name = config['extended_user_profile']['app_name']
    user_class = config['extended_user_profile']['user_class']
    extended_user_model = get_model(app_name, user_class)

# Create ldif string
def write_ldif():
    users = User.objects.all()
    ldif_string = ""
    user_count = 0
    current_uid = uid
    current_gid = gid
    for user in users:
        print "Adding user " + user.username.upper()
        input_string = u"""
dn: cn={username},ou=groups,{domain}
cn: {username}
gidNumber: {gid}
objectClass: top
objectClass: posixGroup

dn: uid={username},ou=people,{domain}
uid: {username}
uidNumber: {uid}
gidNumber: {gid}
cn: {firstname} {lastname}
sn: {lastname}
givenName: {firstname}
displayName: {firstname} {lastname}
objectClass: top
objectClass: person
objectClass: inetOrgPerson
objectClass: organizationalPerson
objectClass: posixAccount
objectClass: shadowAccount
loginShell: /bin/bash
homeDirectory: /home/{username}
"""
        d = {
        'domain': domain,
        'username': user.username,
        'firstname': user.first_name,
        'lastname': user.last_name,
        'gid': str(current_gid),
        'uid': str(current_uid)
        }

        formatted_string = input_string.format(**d)
        if 'attribute_mapping' in config:
            global attributes
            attributes = config['attribute_mapping']
            ldif_string += append_optional_attr(user, formatted_string)
        else:
            ldif_string += formatted_string
        user_count += 1
        current_gid += 1
        current_uid += 1

    write_to_file(ldif_string)
    print "Added " + str(user_count) + " Django users to ldif."

def write_to_file(input_string):
    with open("create_users.ldif", "w") as output_file:
        output_file.write(input_string.encode('utf-8'))

# Check user object for additional attributes
def append_optional_attr(user_obj, ldap_string):
    user = extended_user_model.objects.get(user=user_obj)
    for key in attributes:
        if hasattr(user,key):
            if getattr(user,key) is not None and getattr(user,key) != "":
                ldap_string += attributes[key] + ": "+ getattr(user,key) + "\n"
        elif hasattr(user_obj,key):
            if getattr(user_obj,key) is not None and getattr(user_obj,key) != "":
                ldap_string += attributes[key] + ": "+ getattr(user_obj,key) + "\n"
    return ldap_string

write_ldif()

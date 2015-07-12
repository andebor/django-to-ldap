#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, sys, django, json

# Get config from json
with open('config.json') as config:
    config = json.load(config)
project_dir = config['project_dir']
project_name = config['project_name']
domain = config['domain']

# Connect to django models
sys.path.append(project_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", project_name + ".settings")
from django.conf import settings
django.setup()
from django.contrib.auth.models import User, Group

groups = Group.objects.all()
uid = 10001
start_string = u"""
dn: ou=groups, {domain}
objectClass: top
objectClass: organizationalUnit
ou: groups

dn: ou=people, {domain}
objectClass: top
objectClass: organizationalUnit
ou: people

dn: cn=sudousers,ou=groups,{domain}
objectClass: top
objectClass: posixGroup
gidNumber: 10000
cn: sudousers
"""

ldif_string = start_string.format(domain=domain)
for group in groups:
    group_string = u"""
dn: cn={groupname},ou=groups,{domain}
objectClass: top
objectClass: posixGroup
gidNumber: {uid}
cn: {groupname}
"""
    d = {
        'groupname': group.name,
        'domain': domain,
        'uid': uid
        }
    formatted_string = group_string.format(**d)
    uid += 1
    ldif_string += formatted_string
    print "Added Django group " + group.name + " to ldif"

with open("create_group_structure.ldif", "w") as output_file:
    output_file.write(ldif_string.encode('utf-8'))

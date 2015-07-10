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
complete_string = u""

for group in groups:
    users = group.user_set.all()
    for user in users:
        ldif_string = u"""
dn: cn={groupname},ou=groups,{domain}
changetype: modify
add: member
member: {username},ou=people,{domain}
"""
        d = {
            'groupname': group.name,
            'username': user.username,
            'domain': domain
            }
        formatted_string = ldif_string.format(**d)
        complete_string += formatted_string

with open("add_users_to_groups.ldif", "w") as output_file:
    output_file.write(complete_string.encode('utf-8'))

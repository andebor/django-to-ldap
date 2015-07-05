# django-to-ldap
Useful scripts to convert django users and groups to ldap structure

These scripts can be used to create ldif files based on your django users and groups.
Those ldif files can then be used to add/modify your ldap database.

#### [create_group_structure.py](create_group_structure.py)
Creates the ldap structure with people and groups ou as well as a sudoers group and any existing Django groups.

#### [users_to_ldap.py](users_to_ldap.py)
Creates ldif for adding the Django users to the ldap database.

#### [users_into_groups.py](users_into_groups.py)
Puts users into groups according to django structure.


**Example configs**
```js
// Minimal config
{
	"project_dir": "/path/to/django/project/dir",
	"domain": "dc=example,dc=com",
	"uid_start": 1000,
	"gid_start": 20000,
}

// Advanced config
{
	"project_dir": "/path/to/django/project/dir",
	"domain": "dc=example,dc=com",
	"uid_start": 1000,
	"gid_start": 20000,
	"extended_user_profile": {  // if you have extended the standard user class
		"app_name": "usermanagement", // name of the django app containing the extended user model
		"user_class": "User_profile" // name of the class
	},
	"attribute_mapping": { // maps django attribute names to ldap counter parts
	  "phone_home": "telephoneNumber",
	  "phone_mobile": "mobile",
	  "birth_date": "birthday",
	  "initials": "initials",
	  "email": "mail",
	  "zip_code": "postalCode",
	  "address": "postalAddress"
	}
}


```

# django-to-ldap
Useful scripts to convert django users and groups to ldap structure


**Example configs**
```json
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

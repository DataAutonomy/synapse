Synapse can now have its conditional/extra dependencies installed by pip. This functionality can be used by using `pip install matrix-synapse[feature]`, where feature is a comma separated list with the possible values "email.enable_notifs", "ldap3", "postgres", "saml2", "url_preview", and "test". If you want to install all optional dependencies, you can use "all" instead.

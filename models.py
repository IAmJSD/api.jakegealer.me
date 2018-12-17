from pynamodb.attributes import UnicodeAttribute
from pynamodb.models import Model
# Imports go here.


class U15EmailKeys(Model):
    """Defines the e-mail keys for U15."""
    class Meta:
        table_name = "u15_email_keys"
        region = "eu-west-2"

    key = UnicodeAttribute(hash_key=True)
    email = UnicodeAttribute()

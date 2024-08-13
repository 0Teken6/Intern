import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if not re.findall('[A-Z]', password):
            raise ValidationError(
                _("The password must contain at least one uppercase letter, A-Z."),
                code='password_no_upper',
            )
        if not re.findall('[a-z]', password):
            raise ValidationError(
                _("The password must contain at least one lowercase letter, a-z."),
                code='password_no_lower',
            )
        if not re.findall('[0-9]', password):
            raise ValidationError(
                _("The password must contain at least one digit, 0-9."),
                code='password_no_number',
            )

    def get_help_text(self):
        return _(
            "Your password must contain at least one uppercase letter, one lowercase letter, and one digit."
        )
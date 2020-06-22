from marshmallow import Schema as _Schema
from marshmallow import fields, post_dump, validate


class Schema(_Schema):
    class Meta(_Schema.Meta):
        ordered = True
        strict = True


class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    firstName = fields.String(
        attribute="first_name",
        required=True,
        # strip=True,
        validate=(validate.Length(min=1, max=255)),
    )
    lastName = fields.String(
        attribute="last_name",
        required=True,
        # strip=True,
        validate=(validate.Length(min=1, max=255))
    )
    name = fields.String(dump_only=True)
    urls = fields.List(fields.Nested("UrlSchema"))


class CurrentUserSchema(UserSchema):
    email = fields.String(
        attribute="email_address",
        required=True,
        validate=(validate.Email(), validate.Length(max=255)),
    )
    password = fields.String(
        required=True,
        load_only=True,
        validate=validate.Length(min=8),
    )
    # TODO: check this
    # currentPassword = fields.String(load_only=True)

    recoveryKey = fields.String(
        attribute="recover_key",
        required=True,
        load_only=True,
        validate=validate.Regexp(r"^[\da-fA-F]+$"),
    )


class UrlSchema(Schema):
    SKIP_VALUES = set([None])

    @post_dump
    def remove_skip_values(self, data, *args, **kwargs):
        return {
            key: value for key, value in data.items()
            if value not in self.SKIP_VALUES
        }
    id = fields.Integer(dump_only=True)
    short_url = fields.String()  # TODO: add validation
    long_url = fields.String()
    created = fields.DateTime()
    expires_at = fields.DateTime(required=False)
    visits = fields.Integer()
    user_id = fields.Integer()

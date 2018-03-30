def password_length(form, field):
    if len(field.data) < 6:
        raise ValidationError("Password must have at least 6 characters.")

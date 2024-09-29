def rol_usuario(user):
    if not user.is_superuser:
        return user

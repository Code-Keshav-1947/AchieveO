from owners.models import Owner

def get_current_owner(user):
    """
    Returns the Owner instance associated with the given user.
    If none exists (e.g. for superusers or newly created users), creates a default Owner profile.
    """
    if not user or not user.is_authenticated:
        return None
    try:
        return user.owner
    except Owner.DoesNotExist:
        owner, _ = Owner.objects.get_or_create(
            user=user,
            defaults={
                "name": user.get_full_name() or user.username,
                "email": user.email or f"{user.username}@example.com",
                "mobile_no": "",
            }
        )
        return owner

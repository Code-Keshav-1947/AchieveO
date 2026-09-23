from owners.utils import get_current_owner

def owner(request):
    owner_obj = None
    name = ""
    if request.user.is_authenticated:
        try:
            owner_obj = get_current_owner(request.user)
            if owner_obj:
                name = owner_obj.name
            else:
                name = request.user.get_full_name() or request.user.username
        except Exception:
            name = request.user.username
    return {
        "name": name,
        "current_owner": owner_obj,
    }



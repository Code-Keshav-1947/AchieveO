def owner(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        name = request.user.owner.name
    else:
        name = ""
    return {"name": name}

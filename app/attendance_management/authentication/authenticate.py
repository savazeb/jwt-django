from .hash import matchHashedText

def authenticate(model, id=None, password=None):
    try:
        user = model.objects.get(employee=id)
    except:
        return None
        
    return user if matchHashedText(user.password, password) else None

from rest_framework.permissions import BasePermission

class IsCreator(BasePermission):
    message = "You must be the creator of this cart."

    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or (obj.author == request.user):
            return True
        else:
            return False

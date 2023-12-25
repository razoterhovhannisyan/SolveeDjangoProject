from rest_framework import permissions


class IsParticipantInConversation(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        user = request.user
        return obj.sender == user or obj.receiver == user

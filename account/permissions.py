from rest_framework import permissions
from account.models import Member


class IsTrainer(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        try:
            member = Member.objects.get(pk=request.user)
            return member.is_trainer
        except Member.DoesNotExist:
            return False


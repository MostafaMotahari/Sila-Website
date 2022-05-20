from account.models import User

class AdminMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_admin:
            return super().dispatch(request, *args, **kwargs)


class TopLevelAdminMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.admin_level == 1:
            return super().dispatch(request, *args, **kwargs)


class RefereeMixin():
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser or request.user.is_referee:
            return super().dispatch(request, *args, **kwargs)
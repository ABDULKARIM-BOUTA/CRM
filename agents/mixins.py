from django.contrib.auth.mixins import AccessMixin

class LoginAndOrganizorRequiredMixin(AccessMixin):

    """ override the mixin to verify that the current user is authenticated and an organizor"""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_organizor:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)

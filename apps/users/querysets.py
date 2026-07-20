from apps.common.querysets import SoftDeleteQuerySet

class UserQuerySet(SoftDeleteQuerySet):

    def users(self):
        return self.filter(role='user')

    def owners(self):
        return self.filter(role='owner')

    def admins(self):
        return self.filter(role='admin')
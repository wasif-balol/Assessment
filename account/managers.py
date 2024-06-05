from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password=None):
        if not username:
            raise ValueError('The Username field is required')
        user = self.model(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, first_name, last_name, password=None):
        user = self.create_user(username, first_name, last_name, password)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

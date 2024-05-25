from django.contrib.auth.models import BaseUserManager


class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        создаёт новую учетную запись пользователя
        :param email:
        :param password:
        """
        if not email:
            raise ValueError('Email must be provided')
        # создание экземпляра пользователя
        # метод model ссылается на модель User
        # normalize_email нормализует email-адрес, например, приводит буквы в нужный регистр
        user = self.model(email=self.normalize_email(email))
        # устанавливает пароль
        user.set_password((password))
        # сохраняет пользователя
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

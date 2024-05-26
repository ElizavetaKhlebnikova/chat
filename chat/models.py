from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4

from django.urls import reverse

User = get_user_model()


class Group(models.Model):
    """
    Групповая модель, в которой несколько пользователей
    могут делиться идеями и обсуждать их
    """
    uuid = models.UUIDField(default=uuid4, editable=False)
    name = models.CharField(max_length=30)
    members = models.ManyToManyField(User)

    def __str__(self) -> str:
        return f"Group {self.name}-{self.uuid}"

    def get_absolute_url(self):
        return reverse("group", args=[str(self.uuid)])

    def add_user_to_group(self, user: User):
        """
        Вспомогательная функция для добавления пользователя
        в группу и создания объекта
        """
        # Добавляет указанного пользователя в поле members.
        self.members.add(user)
        # Создает запись в связанном наборе событий (предполагается наличие модели Event с типом "Join"), указывающую, что пользователь присоединился к группе.
        self.event_set.create(type="Join", user=user)
        self.save()

    def remove_user_from_group(self, user: User):
        """
        Функция для удаления членов группы, когда
        они выходят из группы чата
        """
        # Удаляет указанного пользователя из поля members.
        self.members.remove(user)
        # Создает запись в связанном наборе событий (предполагается наличие модели Event с типом "Left"), указывающую, что пользователь покинул группу.
        self.event_set.create(type="Left", user=user)
        self.save()


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self) -> str:
        date = self.timestamp.date()
        time = self.timestamp.time()
        return f"{self.author}:- {self.content} @{date} {time.hour}:{time.minute}"


class Event(models.Model):
    CHOICES = [
        ("Join", "join"),
        ("Left", "left")
    ]
    type = models.CharField(choices=CHOICES, max_length=10)
    description = models.CharField(help_text="A description of the event that occurred",
                                   max_length=50,
                                   editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.description = f"{self.user} {self.type} the {self.group.name} group"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.description}"

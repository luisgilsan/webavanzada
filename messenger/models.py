from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import m2m_changed

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created']

class ThreadManager(models.Manager):

    def find(self, user1, user2):
        queryset = self.filter(users=user1).filter(users=user2)
        if len(queryset) > 0:
            return queryset[0]
        return None

    def find_or_create(self,user1,user2):
        thread = self.find(user1,user2)
        if thread is None:
            thread = Thread.objects.create()
            thread.users.add(user1,user2)
        return thread



class Thread(models.Model):
    users = models.ManyToManyField(User, related_name='threads')
    messages = models.ManyToManyField(Message)
    created = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    objects = ThreadManager()

    class Meta:
        ordering = ['-updated']


def messages_changed(sender, **kwargs):
    instance = kwargs.pop('instance',None)
    action = kwargs.pop('action',None)
    pk_set = kwargs.pop('pk_set',None)
    fake_users = set()
    # Se busca los mensajes de usuarios que no pertencen al hilo
    if action == "pre_add":
        for msg_id in pk_set:
            msg = Message.objects.get(pk=msg_id)
            if msg.user not in instance.users.all():
                fake_users.add(msg_id)
    # Se remueve los mensajes de usuarios que no pertenecen al hilo
    pk_set.difference_update(fake_users)


m2m_changed.connect(messages_changed, sender=Thread.messages.through)


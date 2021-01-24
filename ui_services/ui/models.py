from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.dispatch import receiver
from grpc_pb2s import user_pb2, user_pb2_grpc
import grpc


class User(AbstractBaseUser):
    password = None
    last_login = None
    role_choices = (('PROFESSOR', 'PROFESSOR'), ('ADMIN', 'ADMIN'), ('STUDENT', 'STUDENT'))
    id = models.PositiveIntegerField(primary_key=True, null=False)
    username = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=10, null=False, choices=role_choices)
    USERNAME_FIELD = 'username'


@receiver(models.signals.post_delete, sender=User)
def auto_delete_user(sender, instance, **kwargs):
    print(instance.id)
    with grpc.insecure_channel('localhost:50057') as channel:
        stub = user_pb2_grpc.UserControllerStub(channel)
        user_obj = user_pb2.User(id=instance.id, role=instance.role)
        stub.Destroy(user_obj)


@receiver(models.signals.post_save, sender=User)
def auto_save_user(sender, instance, created, **kwargs):
    if created:
        with grpc.insecure_channel('localhost:50057') as channel:
            stub = user_pb2_grpc.UserControllerStub(channel)
            print(type(instance.id))
            user_obj = user_pb2.User(id=instance.id, role=instance.role)
            response = stub.Create(user_obj)
            print(response.role)
    else:
        try:
            user = User.objects.get(id=instance.id)
            if instance.role != user.role:
                with grpc.insecure_channel('localhost:50057') as channel:
                    stub = user_pb2_grpc.UserControllerStub(channel)
                    user_obj = user_pb2.User(id=instance.id, role=instance.role)
                    stub.Update(user_obj)
        except:
            pass


class Class(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=30, null=False)


class Take(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'class_obj')


class Teach(models.Model):
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    class_obj = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'class_obj')


class File(models.Model):
    file = models.FileField(upload_to='static/files')

from .models import File, User, Class, Take, Teach
from django_grpc_framework import generics
from grpc_pb2s import class_pb2, class_pb2_grpc, file_pb2, file_pb2_grpc
import io
import grpc
from django.core.files.uploadedfile import InMemoryUploadedFile
from google.protobuf import empty_pb2

from django_grpc_framework import services


class FileServices(services.Service):
    def CreateFile(self, request, context):
        file = io.BytesIO(request.content)
        file.seek(0, 2)
        file_data = InMemoryUploadedFile(file, 'file', request.name, None, file.tell(), None)
        obj = File(file=file_data)
        obj.save()
        response = file_pb2.CreateResponse()
        response.id = obj.id
        return response

    def RetrieveFile(self, request, context):
        try:
            file = File.objects.get(id=request.id)
            response = file_pb2.FileURL()
            response.url = file.file.url
            return response
        except:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'File:%s not found!' % request.id)

    def DestroyFile(self, request, context):
        try:
            file = File.objects.get(id=request.id)
            file.delete()
            return empty_pb2.Empty()
        except:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'File:%s not found!' % request.id)


class CourseServices(services.Service):

    def List(self, request, context):
        try:
            user = User.objects.get(id=request.user_id)
            if user.role == "STUDENT":
                list_class = Take.objects.filter(student=user).values_list('class_obj', flat=True)
                response = class_pb2.ClassList()
                response.class_id.extend(list_class)
            elif user.role == "PROFESSOR":
                list_class = Teach.objects.filter(teacher=user).values_list('class_obj', flat=True)
                response = class_pb2.ClassList()
                response.class_id.extend(list_class)
            return response
        except Exception as e:
            print(e)
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'User:%s not found!' % request.user_id)

    def GetCommonClasses(self, request, context):
        try:
            course = Class.objects.get(id=request.class_id)
            user_list = Take.objects.filter(class_obj=course).values_list('student', flat=True)
            course_list = Take.objects.filter(student__in=user_list).values_list('class_obj', flat=True).distinct()
            response = class_pb2.ClassList()
            response.class_id.extend(course_list)
            return response
        except Exception as e:
            self.context.abort(grpc.StatusCode.NOT_FOUND, 'Course:%s not found!' % request.class_id)

    def IsExist(self, request, context):
        is_exist = True
        try:
            course = Class.objects.get(id=request.class_id)
        except Class.DoesNotExist:
            is_exist = False
        response = class_pb2.IsExistResponse()
        response.is_exist = is_exist
        return response


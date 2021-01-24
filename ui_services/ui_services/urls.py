"""ui_services URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from ui.services import FileServices, CourseServices
from ui.views import create_user, delete_user, fill
from grpc_pb2s import file_pb2_grpc, class_pb2_grpc
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('post/', create_user),
    path('delete/<int:pk>/', delete_user),
    path('fill/', fill),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

def grpc_handlers(server):
    file_pb2_grpc.add_FileControllerServicer_to_server(FileServices.as_servicer(), server)
    class_pb2_grpc.add_ClassControllerServicer_to_server(CourseServices.as_servicer(), server)
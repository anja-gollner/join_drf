from .serializers import ContactSerializer, SubtaskSerializer, TaskSerializer
from .models import Contact, Subtask, Task
from rest_framework import viewsets
# from rest_framework.permissions import AllowAny


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    # permission_classes = [AllowAny]


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

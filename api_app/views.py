from .serializers import ContactSerializer, SubtaskSerializer, TaskSerializer
from .models import Contact, Subtask, Task
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .permissions import IsStaffOrSuperUserForTasks, IsAuthenticated, IsSuperUserCRUDIsStaffCRUIsActiveOnlyRead


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsSuperUserCRUDIsStaffCRUIsActiveOnlyRead]


class SubtaskViewSet(viewsets.ModelViewSet):
    queryset = Subtask.objects.all()
    serializer_class = SubtaskSerializer
    permission_classes = [IsStaffOrSuperUserForTasks]


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsStaffOrSuperUserForTasks]


class SummaryView(APIView):
    def get(self, request):
        task_counts = {
            "todo": Task.objects.filter(progress="todo").count(),
            "in-progress": Task.objects.filter(progress="in progress").count(),
            "await-feedback": Task.objects.filter(progress="await feedback").count(),
            "done": Task.objects.filter(progress="done").count(),
            "total-tasks": Task.objects.count(),
            "urgent": Task.objects.filter(priority="urgent").count(),
        }
        urgent_tasks = Task.objects.filter(
            priority="urgent", dueDate__isnull=False).order_by("dueDate")
        if urgent_tasks.exists():
            task_counts["upcoming-deadline"] = urgent_tasks.first().dueDate.strftime("%Y-%m-%d")
        else:
            task_counts["upcoming-deadline"] = None
        return Response(task_counts)

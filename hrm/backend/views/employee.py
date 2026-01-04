from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from ..models.employee import EmployeeRecord, Department
from ..serializers.employee import EmployeeSerializer, DepartmentSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for Employee model"""
    queryset = EmployeeRecord.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def profile(self, request, pk=None):
        """Get employee profile details"""
        employee = self.get_object()
        serializer = self.get_serializer(employee)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_department(self, request):
        """Filter employees by department"""
        department = request.query_params.get('department')
        if department:
            employees = EmployeeRecord.objects.filter(department_name=department)
            serializer = self.get_serializer(employees, many=True)
            return Response(serializer.data)
        return Response({"error": "Department parameter required"}, status=400)


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a department"""
        department = self.get_object()
        employees = EmployeeRecord.objects.filter(department_name=department.name)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class DepartmentListCreateView(generics.ListCreateAPIView):
    """Generic view for Department list and create operations"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


# URL patterns for employee views
urlpatterns = [
    path('', EmployeeViewSet.as_view({'get': 'list', 'post': 'create'}), name='employee-list-create'),
    path('<uuid:pk>/', EmployeeViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='employee-detail'),
    path('<uuid:pk>/profile/', EmployeeViewSet.as_view({'get': 'profile'}), name='employee-profile'),
    path('by-department/', EmployeeViewSet.as_view({'get': 'by_department'}), name='employees-by-department'),
]

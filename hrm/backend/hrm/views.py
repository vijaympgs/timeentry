from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics
from hrm.models.employee import EmployeeRecord
from hrm.models.department import Department
from .serializers import EmployeeSerializer, DepartmentSerializer


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
            employees = EmployeeRecord.objects.filter(department=department)
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
        employees = EmployeeRecord.objects.filter(department=department.name)
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data)


class DepartmentListCreateView(generics.ListCreateAPIView):
    """Generic view for Department list and create operations"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import generics

from ..models.employee import EmployeeRecord
from ..models.department import Department
from ..serializers.employee import EmployeeRecordSerializer
from ..serializers.organizational_unit import DepartmentSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    """ViewSet for Department model"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = []  # Allow unauthenticated access for development

    @action(detail=True, methods=['get'])
    def employees(self, request, pk=None):
        """Get all employees in a department"""
        department = self.get_object()
        employees = EmployeeRecord.objects.filter(department_name=department.name)
        serializer = EmployeeRecordSerializer(employees, many=True)
        return Response(serializer.data)


class DepartmentListCreateView(generics.ListCreateAPIView):
    """Generic view for Department list and create operations"""
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]

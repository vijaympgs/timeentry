from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models.employee import EmployeeRecord
from ..serializers import EmployeeSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """ViewSet for Employee model"""
    queryset = EmployeeRecord.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = []  # Allow unauthenticated access for development
    pagination_class = None  # Disable pagination to return all results

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

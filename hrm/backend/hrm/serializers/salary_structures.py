"""
Salary Structures Serializers for HRM
Following BBP 04.1 Salary Structures specifications
"""

from rest_framework import serializers
from ..models.salary_structures import SalaryStructure, PayGrade


class PayGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PayGrade
        fields = '__all__'


class SalaryStructureSerializer(serializers.ModelSerializer):
    pay_grades = PayGradeSerializer(many=True, read_only=True)
    
    class Meta:
        model = SalaryStructure
        fields = '__all__'

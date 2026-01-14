"""
Audit Trail Serializers for HRM Module
Following T1 Complex Master Template specifications
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from ..models.audit_trail import AuditTrail, AuditTrailConfiguration


class AuditTrailSerializer(serializers.ModelSerializer):
    """Comprehensive audit trail serializer"""
    
    user_email = serializers.EmailField(read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    timestamp_formatted = serializers.SerializerMethodField()
    changes_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditTrail
        fields = [
            'id', 'action', 'action_display', 'model_name', 'model_id', 'company_code',
            'user', 'user_email', 'user_name', 'session_key', 'ip_address', 'user_agent',
            'old_values', 'new_values', 'changed_fields', 'timestamp', 'timestamp_formatted',
            'reason', 'batch_id', 'changes_summary'
        ]
        read_only_fields = ['id', 'timestamp', 'timestamp_formatted', 'changes_summary']
    
    def get_timestamp_formatted(self, obj):
        """Format timestamp for display"""
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_changes_summary(self, obj):
        """Generate a human-readable summary of changes"""
        if obj.action == 'CREATE':
            return f"Created {obj.model_name} with {len(obj.changed_fields)} fields"
        elif obj.action == 'DELETE':
            return f"Deleted {obj.model_name} (had {len(obj.changed_fields)} fields)"
        elif obj.action == 'UPDATE':
            return f"Updated {len(obj.changed_fields)} fields: {', '.join(obj.changed_fields)}"
        elif obj.action == 'VIEW':
            return f"Viewed {obj.model_name}"
        return f"{obj.action} operation on {obj.model_name}"


class AuditTrailListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    
    user_email = serializers.EmailField(read_only=True)
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    action_display = serializers.CharField(source='get_action_display', read_only=True)
    timestamp_formatted = serializers.SerializerMethodField()
    changes_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditTrail
        fields = [
            'id', 'action', 'action_display', 'model_name', 'model_id',
            'user_email', 'user_name', 'timestamp_formatted', 'changes_summary'
        ]
    
    def get_timestamp_formatted(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    def get_changes_summary(self, obj):
        if obj.action == 'CREATE':
            return f"Created {obj.model_name}"
        elif obj.action == 'DELETE':
            return f"Deleted {obj.model_name}"
        elif obj.action == 'UPDATE':
            return f"Updated {len(obj.changed_fields)} fields"
        elif obj.action == 'VIEW':
            return f"Viewed {obj.model_name}"
        return f"{obj.action} operation"


class AuditTrailConfigurationSerializer(serializers.ModelSerializer):
    """Serializer for audit trail configuration"""
    
    class Meta:
        model = AuditTrailConfiguration
        fields = [
            'id', 'model_name', 'is_enabled', 'track_creates', 'track_updates',
            'track_deletes', 'track_views', 'tracked_fields', 'excluded_fields',
            'retention_days', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AuditTrailCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating audit trail entries (internal use)"""
    
    class Meta:
        model = AuditTrail
        fields = [
            'action', 'model_name', 'model_id', 'company_code', 'user', 'user_email',
            'session_key', 'ip_address', 'user_agent', 'old_values', 'new_values',
            'changed_fields', 'reason', 'batch_id'
        ]


class AuditTrailFilterSerializer(serializers.Serializer):
    """Serializer for audit trail filtering parameters"""
    
    model_name = serializers.CharField(required=False)
    action = serializers.ChoiceField(
        choices=AuditTrail.ACTION_CHOICES,
        required=False
    )
    user_id = serializers.IntegerField(required=False)
    company_code = serializers.CharField(required=False)
    date_from = serializers.DateField(required=False)
    date_to = serializers.DateField(required=False)
    model_id = serializers.CharField(required=False)
    changed_fields = serializers.ListField(
        child=serializers.CharField(),
        required=False
    )
    
    def validate(self, attrs):
        """Validate filter parameters"""
        date_from = attrs.get('date_from')
        date_to = attrs.get('date_to')
        
        if date_from and date_to and date_from > date_to:
            raise serializers.ValidationError("date_from must be before date_to")
        
        return attrs


class AuditTrailStatisticsSerializer(serializers.Serializer):
    """Serializer for audit trail statistics"""
    
    total_entries = serializers.IntegerField()
    creates_count = serializers.IntegerField()
    updates_count = serializers.IntegerField()
    deletes_count = serializers.IntegerField()
    views_count = serializers.IntegerField()
    unique_users = serializers.IntegerField()
    unique_models = serializers.IntegerField()
    most_active_user = serializers.DictField()
    most_modified_model = serializers.DictField()
    recent_activity = serializers.ListField(child=serializers.DictField())

"""
Recognition Badges Models for HRM
Following BBP 08.2 Recognition Badges specifications
Aligned with enterprise governance and Olivine UI canon
"""
import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils import timezone
User = get_user_model()

class Badge(models.Model):
    """
    Main badge model for employee recognition
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='badge_company')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='badge_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='badge_updated_by')
    badge_name = models.CharField(max_length=200)
    badge_code = models.CharField(max_length=50)
    badge_description = models.TextField()
    badge_category = models.CharField(max_length=100, choices=[('performance', 'Performance Excellence'), ('teamwork', 'Teamwork & Collaboration'), ('innovation', 'Innovation & Creativity'), ('leadership', 'Leadership'), ('customer_service', 'Customer Service'), ('learning', 'Learning & Development'), ('wellness', 'Wellness & Health'), ('diversity', 'Diversity & Inclusion'), ('sustainability', 'Sustainability'), ('safety', 'Safety'), ('quality', 'Quality'), ('milestone', 'Milestone'), ('values', 'Company Values'), ('custom', 'Custom')])
    badge_type = models.CharField(max_length=50, choices=[('achievement', 'Achievement Badge'), ('behavior', 'Behavior Badge'), ('skill', 'Skill Badge'), ('milestone', 'Milestone Badge'), ('appreciation', 'Appreciation Badge'), ('excellence', 'Excellence Badge'), ('innovation', 'Innovation Badge'), ('leadership', 'Leadership Badge'), ('team', 'Team Badge'), ('custom', 'Custom Badge')])
    badge_tier = models.CharField(max_length=20, choices=[('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold'), ('platinum', 'Platinum'), ('diamond', 'Diamond'), ('legendary', 'Legendary'), ('custom', 'Custom')])
    rarity_level = models.CharField(max_length=20, choices=[('common', 'Common'), ('uncommon', 'Uncommon'), ('rare', 'Rare'), ('epic', 'Epic'), ('legendary', 'Legendary')])
    badge_icon = models.URLField(blank=True)
    badge_color = models.CharField(max_length=20, default='#007bff')
    badge_image_url = models.URLField(blank=True)
    badge_design_template = models.CharField(max_length=100, blank=True)
    points_value = models.IntegerField(default=0)
    is_stackable = models.BooleanField(default=False)
    max_awards_per_employee = models.IntegerField(null=True, blank=True)
    award_criteria = models.JSONField(default=dict, blank=True)
    automatic_award = models.BooleanField(default=False)
    requires_approval = models.BooleanField(default=True)
    eligible_departments = models.JSONField(default=list, blank=True)
    eligible_roles = models.JSONField(default=list, blank=True)
    eligible_levels = models.JSONField(default=list, blank=True)
    min_tenure_months = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('draft', 'Draft'), ('active', 'Active'), ('inactive', 'Inactive'), ('retired', 'Retired'), ('archived', 'Archived')], default='draft')
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    is_permanent = models.BooleanField(default=True)
    validity_months = models.IntegerField(null=True, blank=True)
    expires_on_date = models.DateField(null=True, blank=True)
    cost_per_award = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    budget_code = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_badges'
        verbose_name = 'Badge'
        verbose_name_plural = 'Badges'
        indexes = [models.Index(fields=['company', 'status'], name='idx_badge_status'), models.Index(fields=['company', 'badge_category'], name='idx_badge_category'), models.Index(fields=['company', 'badge_tier'], name='idx_badge_tier')]
        constraints = [models.UniqueConstraint(fields=['company', 'badge_code'], name='uk_badge_code')]
        ordering = ['badge_name']

    def __str__(self):
        return f'{self.badge_name} ({self.badge_code})'

    def clean(self):
        """Validate badge data"""
        if self.points_value and self.points_value < 0:
            raise ValidationError('Points value cannot be negative')
        if self.points_value and self.points_value > 1000:
            raise ValidationError('Points value cannot exceed 1000')
        if self.max_awards_per_employee and self.max_awards_per_employee < 1:
            raise ValidationError('Maximum awards per employee must be at least 1')
        if self.max_awards_per_employee and self.max_awards_per_employee > 100:
            raise ValidationError('Maximum awards per employee cannot exceed 100')
        if self.min_tenure_months and self.min_tenure_months < 0:
            raise ValidationError('Minimum tenure months cannot be negative')
        if not self.is_permanent and (not self.validity_months) and (not self.expires_on_date):
            raise ValidationError('Non-permanent badges must have validity period or expiration date')
        if self.validity_months and self.validity_months < 1:
            raise ValidationError('Validity months must be at least 1')
        if self.cost_per_award and self.cost_per_award < 0:
            raise ValidationError('Cost per award cannot be negative')
        if self.badge_color and (not self.badge_color.startswith('#')):
            raise ValidationError('Badge color must start with #')

class BadgeAward(models.Model):
    """
    Individual badge award records
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='badgeaward_company')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='badgeaward_badge')
    recipient_employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='badgeaward_recipient_employee')
    awarded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='badgeaward_awarded_by')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='badgeaward_approved_by')
    revoked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='badgeaward_revoked_by')
    award_number = models.CharField(max_length=50)
    award_date = models.DateTimeField(auto_now_add=True)
    award_type = models.CharField(max_length=50, choices=[('peer_recognition', 'Peer Recognition'), ('manager_award', 'Manager Award'), ('hr_award', 'HR Award'), ('leadership_award', 'Leadership Award'), ('automatic', 'Automatic Award'), ('milestone', 'Milestone Award'), ('achievement', 'Achievement Award'), ('custom', 'Custom Award')])
    award_reason = models.TextField()
    award_description = models.TextField(blank=True)
    achievement_context = models.JSONField(default=dict, blank=True)
    points_earned = models.IntegerField(default=0)
    reward_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('awarded', 'Awarded'), ('revoked', 'Revoked'), ('expired', 'Expired')], default='pending')
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    shared_on_social_feed = models.BooleanField(default=True)
    expires_date = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    revoked_date = models.DateTimeField(null=True, blank=True)
    revocation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_badge_awards'
        verbose_name = 'Badge Award'
        verbose_name_plural = 'Badge Awards'
        indexes = [models.Index(fields=['company', 'badge'], name='idx_award_badge'), models.Index(fields=['company', 'recipient_employee'], name='idx_award_recipient'), models.Index(fields=['company', 'awarded_by'], name='idx_award_giver'), models.Index(fields=['company', 'status'], name='idx_award_status')]
        constraints = [models.UniqueConstraint(fields=['company', 'award_number'], name='uk_award_number')]
        ordering = ['-award_date']

    def __str__(self):
        return f'{self.badge.badge_name} - {self.recipient_employee}'

    def clean(self):
        """Validate badge award data"""
        if self.points_earned and self.points_earned < 0:
            raise ValidationError('Points earned cannot be negative')
        if self.reward_amount and self.reward_amount < 0:
            raise ValidationError('Reward amount cannot be negative')
        if self.award_date and self.award_date > timezone.now():
            if not self.pk:
                raise ValidationError('Award date cannot be in the future')
        if self.approval_date and self.award_date and (self.approval_date < self.award_date):
            raise ValidationError('Approval date cannot be before award date')
        if self.revoked_date and self.award_date and (self.revoked_date < self.award_date):
            raise ValidationError('Revocation date cannot be before award date')
        if self.expires_date and self.award_date and (self.expires_date < self.award_date):
            raise ValidationError('Expiration date cannot be before award date')

class BadgeNomination(models.Model):
    """
    Badge nomination workflow for peer recognition
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='badgenomination_company')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name='badgenomination_badge')
    nominated_employee = models.ForeignKey('hrm.Employee', on_delete=models.CASCADE, related_name='badgenomination_nominated_employee')
    nominated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='badgenomination_nominated_by')
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='badgenomination_reviewed_by')
    nomination_number = models.CharField(max_length=50)
    nomination_date = models.DateTimeField(auto_now_add=True)
    nomination_reason = models.TextField()
    supporting_evidence = models.JSONField(default=list, blank=True)
    witness_statements = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=[('submitted', 'Submitted'), ('under_review', 'Under Review'), ('approved', 'Approved'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn'), ('expired', 'Expired')], default='submitted')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comments = models.TextField(blank=True)
    rejection_reason = models.TextField(blank=True)
    current_approval_level = models.IntegerField(default=1)
    required_approvals = models.IntegerField(default=1)
    approvals_received = models.IntegerField(default=0)
    support_votes = models.IntegerField(default=0)
    oppose_votes = models.IntegerField(default=0)
    minimum_votes_required = models.IntegerField(default=1)
    nomination_deadline = models.DateTimeField(null=True, blank=True)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'hr_badge_nominations'
        verbose_name = 'Badge Nomination'
        verbose_name_plural = 'Badge Nominations'
        indexes = [models.Index(fields=['company', 'badge'], name='idx_nomination_badge'), models.Index(fields=['company', 'nominated_employee'], name='idx_nomination_recipient'), models.Index(fields=['company', 'nominated_by'], name='idx_nomination_nominator')]
        constraints = [models.UniqueConstraint(fields=['company', 'nomination_number'], name='uk_nomination_number')]
        ordering = ['-nomination_date']

    def __str__(self):
        return f'Nomination: {self.badge.badge_name} - {self.nominated_employee}'

    def clean(self):
        """Validate badge nomination data"""
        if self.current_approval_level and self.current_approval_level < 1:
            raise ValidationError('Current approval level must be at least 1')
        if self.required_approvals and self.required_approvals < 1:
            raise ValidationError('Required approvals must be at least 1')
        if self.approvals_received and self.approvals_received < 0:
            raise ValidationError('Approvals received cannot be negative')
        if self.support_votes and self.support_votes < 0:
            raise ValidationError('Support votes cannot be negative')
        if self.oppose_votes and self.oppose_votes < 0:
            raise ValidationError('Oppose votes cannot be negative')
        if self.minimum_votes_required and self.minimum_votes_required < 1:
            raise ValidationError('Minimum votes required must be at least 1')
        if self.nomination_deadline and self.nomination_deadline < timezone.now():
            raise ValidationError('Nomination deadline cannot be in the past')
        if self.nomination_date and self.nomination_date > timezone.now():
            if not self.pk:
                raise ValidationError('Nomination date cannot be in the future')
        if self.review_date and self.nomination_date and (self.review_date < self.nomination_date):
            raise ValidationError('Review date cannot be before nomination date')

class BadgeCategory(models.Model):
    """
    Badge categories for organization
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='badgecategory_company')
    category_name = models.CharField(max_length=100)
    category_code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'hr_badge_categories'
        verbose_name = 'Badge Category'
        verbose_name_plural = 'Badge Categories'
        constraints = [models.UniqueConstraint(fields=['company', 'category_code'], name='uk_badge_category_code')]

class RecognitionFeed(models.Model):
    """
    Social recognition feed for sharing awards
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    company = models.ForeignKey('hrm.Company', on_delete=models.CASCADE, null=True, blank=True, related_name='recognitionfeed_company')
    badge_award = models.ForeignKey(BadgeAward, on_delete=models.CASCADE, related_name='recognitionfeed_badge_award')
    feed_content = models.TextField()
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    shares_count = models.IntegerField(default=0)

    class Meta:
        db_table = 'hr_recognition_feeds'
        verbose_name = 'Recognition Feed'
        verbose_name_plural = 'Recognition Feeds'
        ordering = ['-created_at']
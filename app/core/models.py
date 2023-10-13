"""
Database models.
"""

from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_field):
        """"Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'

# # from django.utils import timezone
# from django.db import models
# from django.db.models import JSONField
# # from django.contrib.gis.db import models
# # from django.contrib.gis.geos import Polygon
# from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# import uuid
#
#
# # Create your models here.
#
#
# class CityMaster(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4)
#     sub_domain = models.CharField(max_length=255, null=True, blank=True)
#     city_name = models.CharField(max_length=255, null=True, blank=True)
#     country = models.CharField(max_length=255, null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     updated_datetime = models.DateTimeField()
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'city_master'
#
#
# class UserManager(BaseUserManager):
#     def create_user(self, username, password=None):
#         """
#         Creates and saves a User with the given username, password.
#         """
#         if not username:
#             raise ValueError("Users must have an username address")
#
#         user = self.model(
#             username=username,
#             password=password,
#         )
#
#         user.set_password(password)
#         user.save(using=self._db)
#         # created_datetime = timezone.now()
#         return user
#
#     def create_superuser(self, username, password=None):
#         """
#         Creates and saves a superuser with the given username,  password.
#         """
#         user = self.create_user(
#             username,
#             password=password,
#         )
#         user.is_admin = True
#         user.save(using=self._db)
#         return user
#
#
# class User(AbstractBaseUser):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4,
#     editable=False)
#     city_id = models.ForeignKey(CityMaster, null=True,
#                                 on_delete=models.CASCADE)
#     username = models.CharField(unique=True, max_length=150)
#     password = models.CharField(max_length=255, null=True, blank=True)
#     first_name = models.CharField(max_length=255, null=True, blank=True)
#     last_name = models.CharField(max_length=255, null=True, blank=True)
#     is_confirmed = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#     created_datetime = models.DateTimeField(auto_now_add=True)
#     created_by = models.ForeignKey('self', on_delete=models.SET_NULL,
#                                    null=True, related_name='created_users')
#     updated_datetime = models.DateTimeField(auto_now_add=True)
#     updated_by = models.ForeignKey('self', on_delete=models.SET_NULL,
#                                    null=True, related_name='updated_users')
#
#     class Meta:
#         db_table = 'user'
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = []
#
#     def __str__(self):
#         return self.username
#
#     def has_perm(self, perm, obj=None):
#         "DOES USER HAVE PERM?"
#         return self.is_admin
#
#     def has_module_perms(self, app_label):
#         "DOES USER HAVE PERM to view"
#         return True
#
#
# @property
# def is_staff(self):
#     "is the user a member of staff?"
#
#     return self.is_admin
#
#
# class CurbArea(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     # geometry = models.PolygonField(default = Polygon(((0, 0), (0, 1),
#     # (1, 1), (1, 0), (0, 0))))
#     name = models.CharField(max_length=255, null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_area')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_area')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'area'
#
#
# class CurbZone(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     area_id = models.ForeignKey(CurbArea, on_delete=models.CASCADE)
#     # geometry = models.PolygonField(default = Polygon(((0, 0), (0, 1),
#     # (1, 1), (1, 0), (0, 0))))
#     name = models.CharField(max_length=255, null=True, blank=True)
#     user_zone_id = models.CharField(max_length=255, null=True, blank=True)
#     street_name = models.CharField(max_length=255, null=True, blank=True)
#     cross_street_start_name = models.CharField(max_length=255, null=True,
#                                                blank=True)
#     cross_street_end_name = models.CharField(max_length=255, null=True,
#                                              blank=True)
#     length = models.IntegerField(null=True, blank=True)
#     available_space_lengths = JSONField(null=True, blank=True)
#     availability_time = models.DateTimeField(null=True, blank=True)
#     width = models.IntegerField(null=True, blank=True)
#     parking_angle = models.CharField(max_length=255, null=True, blank=True)
#     num_spaces = models.IntegerField(null=True, blank=True)
#     street_side = models.CharField(max_length=2, null=True, blank=True)
#     median = models.BooleanField(default=False)
#     entire_roadway = models.BooleanField(default=False)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_zone')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_zone')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'zone'
#
#
# class CurbSpace(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     zone_id = models.ForeignKey(CurbZone, on_delete=models.CASCADE)
#     # geometry = models.PolygonField(default = Polygon(((0, 0), (0, 1),
#     # (1, 1), (1, 0), (0, 0))))
#     name = models.CharField(max_length=255, null=True, blank=True)
#     space_number = models.IntegerField(null=True, blank=True)
#     length = models.IntegerField()
#     width = models.IntegerField(null=True, blank=True)
#     available = models.BooleanField(default=False)
#     availability_time = models.DateTimeField(null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_space')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_space')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'curb_space'
#
#
# class Policy(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     priority = models.IntegerField()
#     data_source_operator_id = JSONField(null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_policy')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_policy')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'policy'
#
#
# class ZonePolicy(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     zone_id = models.ForeignKey(CurbZone, on_delete=models.CASCADE)
#     policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_zone_policy')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_zone_policy')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'zone_policy'
#
#
# class PolicyRule(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)
#     activity = models.CharField(max_length=255)
#     max_stay = models.IntegerField(null=True, blank=True)
#     max_stay_unit = models.CharField(max_length=255, default='minute')
#     no_return = models.IntegerField(default=0)
#     no_return_unit = models.CharField(max_length=255, default='minute')
#     user_classes = JSONField(null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_policy_rule')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_policy_rule')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'policy_rule'
#
#
# class PolicyTimespan(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     policy_id = models.ForeignKey(Policy, on_delete=models.CASCADE)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     day_of_week = JSONField(null=True, blank=True)
#     day_of_month = JSONField(null=True, blank=True)
#     months = JSONField(null=True, blank=True)
#     time_of_day_start = models.CharField(max_length=2, null=True, blank=True)
#     time_of_day_end = models.CharField(max_length=2, null=True, blank=True)
#     designated_period_except = models.CharField(max_length=2, null=True,
#                                                 blank=True)
#     designated_period = models.CharField(max_length=2, null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_policy_timespan')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_policy_timespan')
#     is_active = models.BooleanField(default=False)
#     street_side = models.CharField(max_length=2, null=True, blank=True)
#
#     class Meta:
#         db_table = 'policy_timespan'
#
#
# class PolicyRate(models.Model):
#     id = models.UUIDField(primary_key=True)
#     city_id = models.ForeignKey(CityMaster, on_delete=models.CASCADE)
#     policy_rule_id = models.ForeignKey(PolicyRule, on_delete=models.CASCADE)
#     rate = models.IntegerField(null=True, blank=True)
#     rate_unit = models.CharField(max_length=255)
#     rate_unit_period = models.CharField(max_length=255)
#     increment_duration = models.IntegerField(null=True, blank=True)
#     increment_amount = models.IntegerField(null=True, blank=True)
#     start_duration = models.IntegerField(null=True, blank=True)
#     end_duration = models.IntegerField(null=True, blank=True)
#     created_datetime = models.DateTimeField()
#     created_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='created_policy_rate')
#     updated_datetime = models.DateTimeField()
#     updated_by = models.ForeignKey(User, on_delete=models.CASCADE,
#                                    related_name='updated_policy_rate')
#     is_active = models.BooleanField(default=False)
#
#     class Meta:
#         db_table = 'policy_rule_rate'

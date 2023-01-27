# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_si = models.CharField(max_length=20)
    region_gu = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'Region'


class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=30)
    school_address1 = models.ForeignKey(Region, models.DO_NOTHING, db_column='school_address1')
    school_address2 = models.CharField(unique=True, max_length=100)
    school_phone = models.CharField(unique=True, max_length=11, blank=True, null=True)
    school_type = models.CharField(max_length=30)
    school_agency = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'School'


class SchoolData(models.Model):
    school_data_id = models.AutoField(primary_key=True)
    school_data_school = models.ForeignKey(School, models.DO_NOTHING, db_column='school_data_school')
    school_studentnum = models.IntegerField(db_column='school_studentNum', blank=True, null=True)  # Field name made lowercase.
    school_yearlybullying = models.IntegerField(db_column='school_yearlyBullying', blank=True, null=True)  # Field name made lowercase.
    school_data_risk = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'School_data'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=30)
    user_passwd = models.CharField(max_length=30)
    user_email = models.CharField(unique=True, max_length=60)
    user_phone = models.CharField(unique=True, max_length=11, blank=True, null=True)
    user_school = models.ForeignKey(School, models.DO_NOTHING, db_column='user_school', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User'


class Video(models.Model):
    video_id = models.AutoField(primary_key=True)
    video_date = models.DateField()
    video_start_time = models.TimeField()
    video_school = models.ForeignKey(School, models.DO_NOTHING, db_column='video_school')
    video_path = models.TextField(blank=True, null=True)
    video_isviolence = models.CharField(db_column='video_isViolence', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Video'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

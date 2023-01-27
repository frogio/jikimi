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
    video_end_time = models.TimeField()
    video_school = models.ForeignKey(School, models.DO_NOTHING, db_column='video_school')
    video_path = models.CharField(max_length=100, blank=True, null=True)
    video_isviolence = models.CharField(db_column='video_isViolence', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Video'
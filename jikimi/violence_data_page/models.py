from django.db import models

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_name = models.CharField(max_length = 150)
    region_environment_score = models.FloatField()

    class Meta:
        managed = True
        db_table = 'Region'


class School(models.Model):
    school_id = models.AutoField(primary_key=True)
    school_name = models.CharField(max_length=30)
    school_address1 = models.ForeignKey(Region, models.DO_NOTHING, db_column='school_address1')
    school_address2 = models.CharField(unique=True, max_length=100)

    class Meta:
        managed = True
        db_table = 'School'


class SchoolData(models.Model):
    school_data_id = models.AutoField(primary_key=True)
    school_data_school = models.ForeignKey(School, models.DO_NOTHING, db_column='school_data_school')
    school_data_harzard_score = models.IntegerField()
    school_data_alleviate_score = models.IntegerField()
    school_data_total_score = models.FloatField()
    school_danger_danger_degree = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'School_data'

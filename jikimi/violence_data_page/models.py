from django.db import models

class Region(models.Model):
    region_id = models.AutoField(primary_key=True)
    region_si = models.CharField(max_length=20)
    region_gu = models.CharField(max_length=20)
    region_singleParent = models.DecimalField(max_digits=10, decimal_places=8)
    region_basicRecipient = models.DecimalField(max_digits=10, decimal_places=8)
    region_incomeMedium = models.DecimalField(max_digits=3, decimal_places=1)
    region_incomeHigh = models.DecimalField(max_digits=3, decimal_places=1)
    region_adultGame = models.IntegerField(11)
    region_homeViolence = models.DecimalField(max_digits=10, decimal_places=9)
    region_dateViolence = models.DecimalField(max_digits=11, decimal_places=10)
    region_averageIncome = models.DecimalField(max_digits=10, decimal_places=8)
    region_multicultural = models.DecimalField(max_digits=11, decimal_places=9)

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
    school_data_education = models.DecimalField(max_digits=5, decimal_places=2)
    school_data_score = models.DecimalField(max_digits=10, decimal_places=8)
    school_data_cluster = models.IntegerField(11)
    school_danger_level = models.CharField(max_length=10)

    class Meta:
        managed = True
        db_table = 'School_data'

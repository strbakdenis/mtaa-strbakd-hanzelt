# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Activities(models.Model):
    name = models.TextField(unique=True)
    activity_type = models.ForeignKey('ActivityTypes', models.DO_NOTHING, db_column='activity_type')
    city = models.ForeignKey('Cities', models.DO_NOTHING, db_column='city')
    address = models.TextField()
    thumbnail_image = models.BinaryField()
    thumbnail_description = models.TextField()
    description = models.TextField()

    class Meta:
        managed = False
        db_table = 'activities'


class ActivityTypes(models.Model):
    type = models.TextField()

    class Meta:
        managed = False
        db_table = 'activity_types'


class Cities(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        managed = False
        db_table = 'cities'


class Images(models.Model):
    activity = models.ForeignKey(Activities, models.DO_NOTHING)
    image = models.BinaryField()

    class Meta:
        managed = False
        db_table = 'images'


class Users(models.Model):

    email_address = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    registration_date = models.DateTimeField()
    token = models.TextField()

    class Meta:
        managed = False
        db_table = 'users'

# Generated by Django 3.0.8 on 2021-05-01 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sehatagahiapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patienttrack',
            name='Duration',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='patienttrack',
            name='Notes',
            field=models.CharField(max_length=1000),
        ),
    ]

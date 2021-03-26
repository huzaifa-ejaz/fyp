# Generated by Django 3.1.7 on 2021-03-20 10:17

from django.db import migrations, models
import django.db.models.deletion
import sehatagahiapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('sehatagahiapp', '0002_auto_20210318_2027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='FilePath',
            field=models.FileField(upload_to='Items/%y', validators=[sehatagahiapp.validators.file_size]),
        ),
        migrations.AlterField(
            model_name='patientprogress',
            name='user_ID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='PatientProgress', to='sehatagahiapp.patienttrack'),
        ),
    ]

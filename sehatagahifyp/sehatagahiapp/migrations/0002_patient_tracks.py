# Generated by Django 3.0.8 on 2021-02-10 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sehatagahiapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='tracks',
            field=models.ManyToManyField(blank=True, related_name='patients', to='sehatagahiapp.Track'),
        ),
    ]

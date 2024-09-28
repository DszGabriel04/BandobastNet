# Generated by Django 5.1.1 on 2024-09-28 05:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_remove_officer_phone_no_remove_supervisor_phone_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='officer',
            name='supervisor_no',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='officer',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile'),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='user_profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.userprofile'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_no',
            field=models.CharField(max_length=15),
        ),
    ]
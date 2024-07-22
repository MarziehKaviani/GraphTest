# Generated by Django 5.0.6 on 2024-07-22 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='endpointcallcount',
            name='method',
            field=models.CharField(default='post', max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='endpointcallcount',
            name='endpoint',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='endpointcallcount',
            unique_together={('endpoint', 'method')},
        ),
    ]
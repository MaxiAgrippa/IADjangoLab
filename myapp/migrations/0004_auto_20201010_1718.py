# Generated by Django 3.1.2 on 2020-10-11 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20201005_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='level',
            field=models.CharField(choices=[('HS', 'High School'), ('UG', 'Undergraduate'), ('PG', 'Postgraduate'), ('ND', 'No Degree')], default='HS', max_length=2),
        ),
    ]

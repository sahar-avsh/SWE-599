# Generated by Django 3.2.12 on 2022-04-22 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20220410_1628'),
        ('mindspace', '0015_auto_20220421_1033'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='sharemindspace',
            unique_together={('mindspace', 'shared_with')},
        ),
    ]

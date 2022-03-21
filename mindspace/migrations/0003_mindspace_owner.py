# Generated by Django 3.2.12 on 2022-03-18 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('mindspace', '0002_auto_20220318_0649'),
    ]

    operations = [
        migrations.AddField(
            model_name='mindspace',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mindspaces', to='profiles.profile'),
        ),
    ]
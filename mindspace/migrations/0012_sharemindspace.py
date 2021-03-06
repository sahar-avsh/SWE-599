# Generated by Django 3.2.12 on 2022-04-19 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_auto_20220410_1628'),
        ('mindspace', '0011_auto_20220405_1119'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShareMindspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.CharField(choices=[('viewer', 'VIEW'), ('editor', 'EDIT'), ('commenter', 'COMMENT')], max_length=9)),
                ('shared_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('mindspace', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='mindspace.mindspace')),
                ('shared_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_by', to='profiles.profile')),
                ('shared_with', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_with', to='profiles.profile')),
            ],
        ),
    ]

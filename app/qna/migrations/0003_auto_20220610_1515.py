# Generated by Django 3.2.13 on 2022-06-10 15:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mindspace', '0020_resource_owner'),
        ('qna', '0002_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='tagged_mindspace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mindspace_answers', to='mindspace.mindspace'),
        ),
        migrations.AlterField(
            model_name='answer',
            name='tagged_resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource_answers', to='mindspace.resource'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tagged_mindspace',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mindspace_questions', to='mindspace.mindspace'),
        ),
        migrations.AlterField(
            model_name='question',
            name='tagged_resource',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource_questions', to='mindspace.resource'),
        ),
    ]

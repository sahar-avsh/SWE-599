# Generated by Django 3.2.13 on 2022-06-02 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='notification_type',
            field=models.CharField(choices=[('AE', 'add_editor'), ('RE', 'remove_editor'), ('AV', 'add_viewer'), ('RV', 'remove_viewer'), ('AC', 'add_commenter'), ('RC', 'remove_commenter'), ('PA', 'post_answer'), ('UA', 'update_answer'), ('UV', 'upvote_answer'), ('DV', 'downvote_answer')], max_length=2),
        ),
    ]

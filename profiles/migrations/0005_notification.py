# Generated by Django 3.2.12 on 2022-04-10 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20220403_1853'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_type', models.CharField(choices=[('AE', 'add_editor'), ('RE', 'remove_editor'), ('AV', 'add_viewer'), ('RV', 'remove_viewer'), ('AC', 'add_commenter'), ('RC', 'remove_commenter'), ('PA', 'post_answer'), ('UA', 'update_answer')], max_length=2)),
                ('read_date', models.DateTimeField(null=True)),
                ('sent_date', models.DateTimeField(auto_now_add=True)),
                ('received_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_notifications', to='profiles.profile')),
                ('sent_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender_notifications', to='profiles.profile')),
            ],
        ),
    ]

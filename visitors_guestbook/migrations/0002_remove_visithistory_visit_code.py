# Generated by Django 2.2.3 on 2019-07-12 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('visitors_guestbook', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visithistory',
            name='visit_code',
        ),
    ]

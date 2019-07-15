# Generated by Django 2.2.3 on 2019-07-15 13:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('visitors_guestbook', '0002_remove_visithistory_visit_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visithistory',
            name='check_in_date',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='check_out_date',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='deleted',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='visithistory',
            name='deleted_date',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='deleted',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='visitor',
            name='deleted_date',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='visitordetailchangehistory',
            name='date_created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='visitordetailchangehistory',
            name='deleted',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AlterField(
            model_name='visitordetailchangehistory',
            name='deleted_date',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AlterField(
            model_name='visitordetailchangehistory',
            name='field',
            field=models.CharField(choices=[('name', 'Visitor Name'), ('address', 'Visitor Address')], max_length=100),
        ),
    ]

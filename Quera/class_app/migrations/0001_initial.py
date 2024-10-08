# Generated by Django 5.1.1 on 2024-10-02 09:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account_app', '0001_initial'),
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('unique_id', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('signup_type', models.CharField(choices=[('P', 'Password'), ('I', 'Invitation Link')], max_length=1)),
                ('start_register_date', models.DateField(blank=True, null=True)),
                ('end_register_date', models.DateField(blank=True, null=True)),
                ('forum', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_app.forum')),
                ('mentors', models.ManyToManyField(related_name='Private_Mentors', to='account_app.account')),
                ('owners', models.ManyToManyField(related_name='Private_Owners', to='account_app.account')),
                ('students', models.ManyToManyField(related_name='Private_Students', to='account_app.account')),
                ('tasks', models.ManyToManyField(blank=True, to='task_app.task')),
            ],
        ),
        migrations.CreateModel(
            name='PublicClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('unique_id', models.CharField(max_length=50)),
                ('capacity', models.PositiveIntegerField(blank=True, null=True)),
                ('start_register_date', models.DateField(blank=True, null=True)),
                ('end_register_date', models.DateField(blank=True, null=True)),
                ('forum', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='account_app.forum')),
                ('mentors', models.ManyToManyField(related_name='Public_Mentors', to='account_app.account')),
                ('owners', models.ManyToManyField(related_name='Public_Owners', to='account_app.account')),
                ('students', models.ManyToManyField(related_name='Public_Students', to='account_app.account')),
                ('tasks', models.ManyToManyField(blank=True, to='task_app.task')),
            ],
        ),
    ]

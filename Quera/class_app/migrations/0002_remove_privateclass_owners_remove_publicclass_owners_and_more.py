# Generated by Django 5.1.1 on 2024-10-02 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0002_alter_account_user'),
        ('class_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='privateclass',
            name='owners',
        ),
        migrations.RemoveField(
            model_name='publicclass',
            name='owners',
        ),
        migrations.AddField(
            model_name='privateclass',
            name='teachers',
            field=models.ManyToManyField(related_name='Private_Teachers', to='account_app.account'),
        ),
        migrations.AddField(
            model_name='publicclass',
            name='teachers',
            field=models.ManyToManyField(related_name='Public_Teachers', to='account_app.account'),
        ),
    ]

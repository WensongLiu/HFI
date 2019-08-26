# Generated by Django 2.2.4 on 2019-08-25 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Users',
            fields=[
                ('userID', models.AutoField(primary_key=True, serialize=False)),
                ('emailAddress', models.EmailField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]

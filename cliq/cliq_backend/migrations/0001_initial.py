# Generated by Django 2.2.1 on 2019-05-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=512)),
                ('desc', models.CharField(max_length=1024)),
                ('owner', models.CharField(max_length=30)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('lastkey', models.CharField(max_length=64)),
                ('ctime', models.DateTimeField(auto_now_add=True)),
                ('ltime', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]

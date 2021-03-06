# Generated by Django 3.0.4 on 2020-03-05 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipoWatcher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('link', models.CharField(max_length=150)),
                ('checked', models.BooleanField(default=False)),
                ('downloaded', models.DateField(blank=True, max_length=100, null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Config',
        ),
        migrations.AddField(
            model_name='watcher',
            name='available',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='watcher',
            name='threshold',
            field=models.IntegerField(default=5),
        ),
    ]

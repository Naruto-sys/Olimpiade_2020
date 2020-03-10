# Generated by Django 3.0.4 on 2020-03-04 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Indications',
            fields=[
                ('town', models.IntegerField(primary_key=True, serialize=False)),
                ('district', models.IntegerField(default=0)),
                ('house', models.IntegerField(default=0)),
                ('flat', models.IntegerField(default=0)),
                ('tempreture', models.IntegerField(default=0)),
            ],
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-28 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='types',
            fields=[
                ('typeid', models.IntegerField()),
                ('qtype', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
        ),
    ]

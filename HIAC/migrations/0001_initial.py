# Generated by Django 4.0.5 on 2022-08-04 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=50)),
                ('transaction_date', models.DateTimeField()),
                ('transaction_balance', models.IntegerField()),
                ('transaction_detail', models.CharField(max_length=70)),
                ('transaction_memo', models.CharField(blank=True, max_length=70, null=True)),
            ],
        ),
    ]
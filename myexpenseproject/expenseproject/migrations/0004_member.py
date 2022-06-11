# Generated by Django 3.1.3 on 2022-06-01 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('expenseproject', '0003_delete_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
                ('money', models.IntegerField(default=200)),
                ('money_spent_today', models.IntegerField(default=0)),
                ('money_spent_this_month', models.IntegerField(default=0)),
                ('money_spent_this_year', models.IntegerField(default=0)),
            ],
        ),
    ]
# Generated by Django 4.2.4 on 2023-09-16 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_birth_date_alter_customuser_city_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='user_categories', to='accounts.category'),
        ),
    ]
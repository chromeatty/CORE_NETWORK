# Generated by Django 5.1.2 on 2024-11-02 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('requests_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='request',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('water', 'Water'), ('clothing', 'Clothing'), ('shelter', 'Shelter'), ('medical', 'Medical Supplies'), ('other', 'Other')], default='Other', max_length=50),
        ),
        migrations.AlterField(
            model_name='request',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='Pending', max_length=11),
        ),
        migrations.AlterField(
            model_name='request',
            name='urgency',
            field=models.CharField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], default='Low', max_length=10),
        ),
    ]

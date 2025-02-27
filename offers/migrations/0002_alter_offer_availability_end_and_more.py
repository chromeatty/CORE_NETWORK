# Generated by Django 5.1.2 on 2024-11-02 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='availability_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='availability_start',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('water', 'Water'), ('clothing', 'Clothing'), ('shelter', 'Shelter'), ('medical', 'Medical Supplies'), ('other', 'Other')], max_length=50),
        ),
        migrations.AlterField(
            model_name='offer',
            name='description',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='quantity',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='offer',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('in_progress', 'In Progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=11),
        ),
        migrations.AlterField(
            model_name='offer',
            name='title',
            field=models.CharField(max_length=100),
        ),
    ]

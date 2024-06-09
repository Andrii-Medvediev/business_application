# Generated by Django 5.0.6 on 2024-06-06 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccountCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('icon_name', models.CharField(max_length=50)),
                ('bg_color', models.CharField(max_length=7)),
            ],
            options={
                'verbose_name': 'Категорія рахунків',
                'verbose_name_plural': 'Категорії рахунків',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('initials', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Валюта',
                'verbose_name_plural': 'Валюти',
            },
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='pdfs/')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документи',
            },
        ),
        migrations.CreateModel(
            name='ExpenseCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('icon_name', models.CharField(max_length=50)),
                ('bg_color', models.CharField(max_length=7)),
            ],
            options={
                'verbose_name': 'Категорія витрат',
                'verbose_name_plural': 'Категорії витрат',
            },
        ),
        migrations.CreateModel(
            name='IncomeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category_name', models.CharField(max_length=50)),
                ('icon_name', models.CharField(max_length=50)),
                ('bg_color', models.CharField(max_length=7)),
            ],
            options={
                'verbose_name': 'Категорія доходів',
                'verbose_name_plural': 'Категорії доходів',
            },
        ),
    ]

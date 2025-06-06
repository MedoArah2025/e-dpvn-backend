# Generated by Django 5.2.1 on 2025-05-14 21:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0001_initial'),
        ('units', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeclarationVol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brouillon', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('date_plainte', models.DateField()),
                ('type_vol', models.CharField(choices=[('Vol simple', 'Vol simple'), ('Vol aggravé', 'Vol aggravé'), ("Vol à l'arraché", "Vol à l'arraché"), ('Agression suivie de vol', 'Agression suivie de vol')], max_length=100)),
                ('nombre_vol', models.IntegerField(default=0)),
                ('quartier', models.CharField(blank=True, max_length=255, null=True)),
                ('unite', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='units.unite')),
            ],
            options={
                'ordering': ['-created_at'],
                'abstract': False,
            },
        ),
    ]

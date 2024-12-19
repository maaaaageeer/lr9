# Generated by Django 5.1.4 on 2024-12-19 17:00

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BonusLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_name', models.CharField(max_length=20, unique=True)),
                ('spending_threshold', models.DecimalField(decimal_places=2, max_digits=10)),
                ('cashback_percentage', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='UserBonuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_spending', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.bonuslevel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bonuses', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

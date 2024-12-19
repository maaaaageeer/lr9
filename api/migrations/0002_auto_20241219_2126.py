from django.db import migrations, transaction


def populate_data(apps, schema_editor):
    BonusLevel = apps.get_model('api', 'BonusLevel')
    UserBonuses = apps.get_model('api', 'UserBonuses')
    User = apps.get_model('auth', 'User')
    with transaction.atomic():
        if not User.objects.filter(username='admin').exists():
            user = User.objects.create_superuser(username='admin',
                                                 email='admin@mail.ru',
                                                 password='admin')
        else:
            user = User.objects.get(username='admin')

        silver_level = BonusLevel.objects.create(level_name='Серебряный', spending_threshold=0,
                                                 cashback_percentage=3)
        gold_level = BonusLevel.objects.create(level_name='Золотой', spending_threshold=5000, cashback_percentage=5)
        platinum_level = BonusLevel.objects.create(level_name='Платиновый', spending_threshold=10000,
                                                   cashback_percentage=10)
        UserBonuses.objects.create(user=user, current_spending=3000, level=silver_level)


class Migration(migrations.Migration):
    dependencies = [
        ('api', '0001_initial'),  # Замените на предыдущую миграцию если есть
    ]

    operations = [
        migrations.RunPython(populate_data),
    ]

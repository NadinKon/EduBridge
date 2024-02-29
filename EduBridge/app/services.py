from django.db.models import Count


def add_user_to_group(user, product):
    # Получаем группы, отсортированные по количеству пользователей
    groups = product.groups.annotate(user_count=Count("users")).order_by("user_count")

    for group in groups:
        if group.user_count < group.max_users:
            group.users.add(user)
            break
    else:
        # Если все группы полные, реализовать логику создания новой группы или исключения
        print("Нет доступных групп или нужно перераспределение")


# Функция перераспределения пользователей по группам
def redistribute_users(product):
    if not product.has_started:
        all_users = [user for group in product.groups for user in group.users.all()]

        # Очищаем всех пользователей из групп
        for group in product.groups.all():
            group.users.clear()

        # Перераспределение пользователей
        users_per_group = len(all_users) // product.groups.count()
        extra_users = len(all_users) % product.groups.count()

        user_index = 0
        for group in product.groups.all():
            for _ in range(users_per_group + (1 if extra_users > 0 else 0)):
                if user_index < len(all_users):
                    group.users.add(all_users[user_index])
                    user_index += 1
            if extra_users > 0:
                extra_users -= 1

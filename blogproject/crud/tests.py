from django.test import TestCase
from django.urls import reverse

from .models import Item


class ItemCreateTests(TestCase):
    """CREATE"""

    # Страница формы создания открывается
    def test_create_page_opens(self):
        response = self.client.get(reverse('crud:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'crud/item_form.html')

    # POST с корректными данными создаёт запись и делает редирект
    def test_create_valid_data(self):
        response = self.client.post(reverse('crud:create'),
                                    {'title': 'Новая', 'description': 'Текст'})
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.get()
        self.assertRedirects(response, item.get_absolute_url())

    # POST с пустым названием не создаёт запись, форма показывает ошибку
    def test_create_invalid_data(self):
        response = self.client.post(reverse('crud:create'), {'title': ''})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 0)
        self.assertTrue(response.context['form'].errors)


class ItemReadTests(TestCase):
    """READ (список и деталь)"""

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(title='Запись 1', description='Описание 1')

    # Список открывается и содержит запись
    def test_list_contains_item(self):
        response = self.client.get(reverse('crud:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Запись 1')

    # Пустой список показывает заглушку
    def test_list_empty(self):
        Item.objects.all().delete()
        response = self.client.get(reverse('crud:list'))
        self.assertContains(response, 'Записей пока нет.')

    # Деталь существующей записи открывается
    def test_detail_existing(self):
        response = self.client.get(self.item.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Описание 1')

    # Деталь несуществующей записи даёт 404
    def test_detail_not_found(self):
        response = self.client.get(reverse('crud:detail', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)


class ItemUpdateTests(TestCase):
    """UPDATE"""

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(title='Старое', description='Текст')

    # Форма редактирования открывается и содержит старые данные
    def test_update_page_prefilled(self):
        response = self.client.get(reverse('crud:update', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Старое')

    # POST меняет данные в базе
    def test_update_changes_data(self):
        url = reverse('crud:update', kwargs={'pk': self.item.pk})
        response = self.client.post(url, {'title': 'Новое', 'description': 'Другой текст'})
        self.assertRedirects(response, self.item.get_absolute_url())
        self.item.refresh_from_db()
        self.assertEqual(self.item.title, 'Новое')

    # Редактирование несуществующей записи даёт 404
    def test_update_not_found(self):
        response = self.client.get(reverse('crud:update', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)


class ItemDeleteTests(TestCase):
    """DELETE"""

    @classmethod
    def setUpTestData(cls):
        cls.item = Item.objects.create(title='Удаляемая')

    # Страница подтверждения удаления открывается
    def test_delete_page_opens(self):
        response = self.client.get(reverse('crud:delete', kwargs={'pk': self.item.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Удаляемая')

    # POST удаляет запись и ведёт на список
    def test_delete_removes_item(self):
        response = self.client.post(reverse('crud:delete', kwargs={'pk': self.item.pk}))
        self.assertRedirects(response, reverse('crud:list'))
        self.assertFalse(Item.objects.filter(pk=self.item.pk).exists())

    # Удаление несуществующей записи даёт 404
    def test_delete_not_found(self):
        response = self.client.post(reverse('crud:delete', kwargs={'pk': 9999}))
        self.assertEqual(response.status_code, 404)

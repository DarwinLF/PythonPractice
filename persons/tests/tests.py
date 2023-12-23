# from django.test import TestCase, Client
# from django.urls import reverse
# from django.db import IntegrityError

# from datetime import date

# from .models import Person
# from mysite.function import validateRnc

# # Create your tests here.

# class PersonAddViewTests(TestCase):
#     def setUp(self):
#         self.url = reverse('persons:person_add')
#         self.client = Client()

#     #change in the future
#     def test_future_birthday(self):
#         data = create_person('Darwin', 'Lantigua Fermin', '402-307960-', date(2030, 1, 8))
#         response = self.client.post(self.url, data, follow=True)
#         self.assertFormError(response, 'form', 'birthday', 'The birthday can\'t be in the future')


# def create_person(first_name, last_name, rnc, birthday):
#     return {
#         'first_name': first_name,
#         'last_name': last_name,
#         'rnc': rnc,
#         'birthday': birthday,
#     }

# class PersonEditViewTest(TestCase):
#     def setUp(self):
#         self.person1 = Person.objects.create(first_name='Darwin', last_name='Lantigua', rnc='402-3070960-8', birthday=date(2000, 1, 8))
#         self.person2 = Person.objects.create(first_name='John', last_name='Doe', rnc='402-3070960-7', birthday=date(1999, 2, 12))
#         self.url = reverse('persons:person_edit', args=[self.person2.pk])
#         self.client = Client()

# class PersonDeleteViewTest(TestCase):
#     def setUp(self):
#         self.person = Person.objects.create(first_name='Darwin', last_name='Lantigua', rnc='402-3070960-8', birthday=date(2000, 1, 8))
#         self.client = Client()

#     def test_delete(self):
#         url = reverse('persons:person_delete', args=[self.person.pk])

#         # Fetch the form for updating the person
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'persons/confirm_delete.html')

#         # Submit the deletion form
#         response = self.client.post(url, follow=True)

#         # Check if the person is deleted in the database
#         self.assertEqual(response.status_code, 200)
#         self.assertTemplateUsed(response, 'persons/index.html')

#         # Ensure the person is no longer in the database
#         self.assertFalse(Person.objects.filter(pk=self.person.pk).exists())
        
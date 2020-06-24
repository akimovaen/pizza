from django.test import TestCase, Client
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from django.utils import timezone
from django.utils.formats import localize

from .models import *
from .views import *

# Create your tests here.

class ModelsTestCase(TestCase):

    def setUp(self):
        m1 = Menu.objects.create(name='Menu_1')
        i1 = Items.objects.create(name='Items_1', menu=m1, trait="S", price=1.00)
        user = User.objects.create_user('test', 'test@test.com', 'test')
        order = Order.objects.create(person=user, number=1)

    def tearDown(self):
        m1 = Menu.objects.get(name="Menu_1")
        m1.delete()
        user = User.objects.get(username='test')
        user.delete()
    
    def test_valid_trait(self):
        test = Items.objects.get(trait = 'S')
        self.assertTrue(test.is_valid_trait())

    def test_invalid_trait(self):
        m = Menu.objects.get(name = 'Menu_1')
        with self.assertRaises(ValidationError):
            i2 = Items.objects.create(name='Items_2', menu=m, trait="T", price=1.00)

    def test_order_default_status(self):
        order = Order.objects.get(number=1)
        self.assertEqual(order.status, "P")

    def test_order_default_placing_time(self):
        order = Order.objects.get(number=1)
        self.assertEqual(localize(order.placing_time), localize(timezone.now()))
        

class RegisterTestCase(TestCase):

    def setUp(self):
       self.client = Client()

    def test_get_status_code_and_view(self):
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, register_view)
        
    def test_get_templates(self):
        response = self.client.get("/register")
        templates_list = ['orders/base.html', 'orders/register.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)

    def test_valid_form_full_data(self):
        register_data = {
            "username": 'test',
            "email": 'test@test.com',
            "password": 'test',
            "first_name": 'test',
            "last_name": 'test'
        }
        response = self.client.post("/register", register_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, register_view)
        
        user = User.objects.get(username='test')
        self.assertEqual(user.email, 'test@test.com')        
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_valid_form_empty_first_and_last_names(self):
        register_data = {
            "username": 'test',
            "email": 'test@test.com',
            "password": 'test',
            "first_name": '',
            "last_name": ''
        }
        response = self.client.post("/register", register_data)
        user = User.objects.get(username='test')
        self.assertEqual(user.email, 'test@test.com')        
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_valid_post_templates(self):
        register_data = {
            "username": 'test',
            "email": 'test@test.com',
            "password": 'test',
            "first_name": '',
            "last_name": ''
        }
        response = self.client.post("/register", register_data)
        templates_list = ['orders/base.html', 'orders/index.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)

    def test_invalid_form_without_password(self):
        response = self.client.post("/register",
                {"username": 'test', "email": 'test@test.com'})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='test')

    def test_invalid_form_empty_password(self):
        response = self.client.post("/register",
                {"username": 'test', "email": 'test@test.com', "password": ''})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='test')

    def test_invalid_form_without_email(self):
        response = self.client.post("/register",
                {"username": 'test', "password": 'test'})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='test')

    def test_invalid_form_empty_email(self):
        response = self.client.post("/register",
                {"username": 'test', "email": '', "password": 'test'})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(username='test')

    def test_invalid_form_without_username(self):
        response = self.client.post("/register",
                {"email": 'test@test.com', "password": 'test'})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(email='test@test.com')

    def test_invalid_form_empty_username(self):
        response = self.client.post("/register",
                {"username": '', "email": 'test@test.com', "password": 'test'})
        with self.assertRaises(ObjectDoesNotExist):
            user = User.objects.get(email='test@test.com')

    def test_invalid_form_without_first_and_last_name(self):
        with self.assertRaises(IntegrityError):
            response = self.client.post("/register",
            {"username": 'test', "email": 'test@test.com', "password": 'test'})

    def test_invalid_post_templates(self):
        response = self.client.post("/register", {"username": 'test'})
        templates_list = ['orders/base.html', 'orders/register.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)


class LoginTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        user = User.objects.create_user('test3', 'test3@test.com', 'test3')
        user.save()

    @classmethod
    def tearDownClass(cls):
        user = User.objects.get(username='test3')
        user.delete()

    def setUp(self):
        self.client = Client()

    def test_get_status_code_and_view(self):
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, login_view)

    def test_get_templates(self):
        response = self.client.get("/login")
        templates_list = ['orders/base.html', 'orders/login.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)

    def test_valid_login_form(self):
        response = self.client.post("/login", {"username": 'test3', "password": 'test3'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.resolver_match.func, login_view)

    def test_invalid_form_invalid_username(self):
        response = self.client.post("/login", {"username": 'test1', "password": 'test3'})
        self.assertNotEqual(response.status_code, 302)

    def test_invalid_form_invalid_password(self):
        response = self.client.post("/login", {"username": 'test3', "password": 'test1'})
        self.assertNotEqual(response.status_code, 302)

    def test_invalid_form_without_username(self):
        response = self.client.post("/login", {"password": 'test3'})
        self.assertNotEqual(response.status_code, 302)

    def test_invalid_form_empty_username(self):
        response = self.client.post("/login", {"username": '',"password": 'test3'})
        self.assertNotEqual(response.status_code, 302)

    def test_invalid_form_without_password(self):
        response = self.client.post("/login", {"username": 'test3'})
        self.assertNotEqual(response.status_code, 302)
    
    def test_invalid_form_empty_password(self):
        response = self.client.post("/login", {"username": 'test3',"password": ''})
        self.assertNotEqual(response.status_code, 302)

    def test_valid_post_templates(self):
        response = self.client.post("/login", {"username": 'test3', "password": 'test3'})
        templates_list = ['orders/base.html', 'orders/index.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)

    def test_invalid_post_templates(self):
        response = self.client.post("/login", {"username": 'test1', "password": 'test1'})
        templates_list = ['orders/base.html', 'orders/login.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)

    def test_logout_get_status_code_and_view(self):
        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.resolver_match.func, logout_view)

    def test_logout_templates(self):
        response = self.client.get("/logout")
        templates_list = ['orders/base.html', 'orders/login.html']
        templates = response.templates
        for template in templates:
            self.assertIn(template.name, templates_list)


class DisplayMenuTestCase(TestCase):

    def setUp(self):
        m2 = Menu.objects.create(name='Menu_2')
        i1 = Items.objects.create(name='Items_1', menu=m2, trait="S", price=1.00)
        i2 = Items.objects.create(name='Items_1', menu=m2, trait="L", price=2.00)
        i3 = Items.objects.create(name='Items_2', menu=m2, trait="A", price=3.00)
        i4 = Items.objects.create(name='Items_3', menu=m2, price=3.00)
        i5 = Items.objects.create(name='Items_4', menu=m2)
       
    def test_count_dishes(self):
        dishes = Items.objects.filter(menu=1)
        self.assertEqual(dishes.count(), 5)

    def test_count_dishes_depend_on_components(self):
        dishes = Items.objects.filter(menu=1)    
        trait = 0
        price = 0
        name = 0
        for dish in dishes:
            if dish.trait:
                trait += 1
            elif dish.price:
                price += 1
            else:
                name += 1
        self.assertEqual(trait, 3)
        self.assertEqual(price, 1)
        self.assertEqual(name, 1)
    
    def test_display_menu(self):
        data = display_menu()
        self.assertEqual(len(data[0]['dishes']), 4)
        

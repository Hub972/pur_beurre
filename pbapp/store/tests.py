from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from mock import patch
import json

from .request_.offs_req import AllRequests
from .models import ProductsNutriTypeA, Favorite


# Create your tests here.
class IndexPageTestCase(TestCase):
    def test_index_page(self):
        response = self.client.get(reverse('store:index'))
        self.assertEqual(response.status_code, 200)


class LoginTestDetailCase(TestCase):
    def setUp(self):
        self.contact = User.objects.create_user(username="marc", email="marc@mail.com")
        self.bad_user = 'jean_marc'

    def test_if_user_exist(self):
        name = self.contact.username
        email = self.contact.email
        passw = self.contact.password
        user = User.objects.get_by_natural_key("marc")
        self.assertEqual(user.email, email)

    def test_if_user_dont_exist(self):
        name = self.contact.username
        self.assertNotEqual(self.bad_user, name)

    def test_if_user_logout(self):
        response = self.client.get(reverse('store:logOut'))
        self.assertEqual(response.status_code, 302)


class DisplayResultProductSearch(TestCase):
    def setUp(self):
        self.productsBadItem = ProductsNutriTypeA.objects.filter(category="blal")
        self.productEmptyItem = ProductsNutriTypeA.objects.filter(category='')
        self.productsGoodItem = ProductsNutriTypeA.objects.filter(category='Meat')

    def test_result_return_200(self):
        response = self.client.post(reverse('store:search'))
        self.assertEqual(response.status_code, 200)

    def test_result_return_bad(self):
        response = self.client.post(reverse('store:search'))
        self.assertQuerysetEqual(self.productsBadItem, self.productEmptyItem)

    def test_result_return_good(self):
        response = self.client.post(reverse('store:search'))
        self.assertNotEquals(self.productsGoodItem, self.productsBadItem)


class AddProductToFavorite(TestCase):
    def setUp(self):
        self.contact = User.objects.create_user(username="polo", email="polo@mail.com")
        self.prd = Favorite(name='eau', generic_name='eau', categorie='water', nutriscore='a', picture='picture', id_user=self.contact)
        self.prd.save()

    def test_return_302(self):
        response = self.client.post(reverse('store:show'))
        self.assertEqual(response.status_code, 302)

    def test_product_in_db(self):
        product = Favorite.objects.get(id_user=self.prd.id_user)
        self.assertEquals(product.name, 'eau')


class MockCase(TestCase):
    BADRESULT = json.dumps({"count": 0, "page_size": "20", "products": [], "skip": 0, "page": "1"})
    RESULT = json.dumps({"page_size": "20", "count": 204, "products": [
        {"nutrition_score_beverage": 0, "allergens": "NOISETTES, LAIT, LACTOSÉRUM, SOJA",
         "brands_tags": ["ferrero", "nutella"], "unique_scans_n": 727, "additives_n": 1, "product_name": "Nutella",
         "data_sources": "Database - FoodRepo / openfood.ch, Databases, Producer - Ferrero, Producers, App - yuka, Apps",
         "no_nutrition_data": "", "selected_images": {"front": {
            "display": {"fr": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.400.jpg"},
            "thumb": {"fr": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.100.jpg"},
            "small": {"fr": "https://static.openfoodfacts.org/images/products/301/762/042/2003/front_fr.139.200.jpg"}}}}]})

    @patch('store.request_.offs_req.AllRequests.search_product_item', return_value=RESULT)
    def test_offs_item_return(self, *args, **kwargs):
        req = AllRequests.search_product_item('Nutella')
        req = json.loads(req)
        self.assertEqual(req['count'], 204)

    @patch('store.request_.offs_req.AllRequests.code_request', return_value=RESULT)
    def test_offs_code_return(self, *args, **kwargs):
        req = AllRequests.code_request(112233445433)
        req = json.loads(req)
        self.assertEqual(req['page_size'], '20')

    @patch('store.request_.offs_req.AllRequests.search_product_item', return_value=BADRESULT)
    def test_offs_bad_item_return(self, *args, **kwargs):
        req = AllRequests.search_product_item('hsfsgg')
        req = json.loads(req)
        self.assertEqual(req['count'], 0)

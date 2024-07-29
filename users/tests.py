from django.test import TestCase
from .models import Request, CustomerProfile, CustomUser
from store.models.product import Product, Category

class RequestSignalTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@email.com', password='12345')
        self.profile = CustomerProfile.objects.create(user=self.user)

    def test_create_product_on_request_creation(self):
        request = Request.objects.create(
            requester=self.profile
        )

        # Retrieve the newly created product
        product = Product.objects.get(id=request.product.id)

        # Verify the product attributes
        self.assertEqual(product.category.name, 'Requested')
        self.assertEqual(product.posted_by, self.user)
        self.assertEqual(product.status, 'requested')

    def test_signal_creates_product(self):
        # Ensure no products exist initially
        self.assertEqual(Product.objects.count(), 0)

        # Create a request
        request = Request.objects.create(
            requester=self.profile
        )

        # Check that a product has been created
        self.assertEqual(Product.objects.count(), 1)
        product = Product.objects.first()

        # Verify the product attributes
        self.assertEqual(product.category.name, 'Requested')
        self.assertEqual(product.posted_by, self.user)
        self.assertEqual(product.status, 'requested')

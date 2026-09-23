from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from owners.models import Owner
from customers.models import Customer
from products.models import Product
from orders.models import Order


class AchieveOTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.owner = Owner.objects.create(
            user=self.user,
            name="Test Press",
            email="press@example.com",
            mobile_no="9876543210",
        )
        self.client = Client()
        self.client.login(username="testuser", password="password123")

        self.customer = Customer.objects.create(
            name="Acme Corp",
            mobile_no="9998887770",
            email="acme@example.com",
            address="Delhi",
            owner=self.owner,
        )

        self.product = Product.objects.create(
            name="Visiting Cards",
            price=200,
            cost_price=120,
            stocks=1000,
            owner=self.owner,
        )

        self.order = Order.objects.create(
            name="500 Cards Order",
            product=self.product,
            customer=self.customer,
            quantity=3,
            advance=200,
            owner=self.owner,
            status="printing",
        )

    def test_financial_calculations(self):
        # 3 * 200 = 600 total
        self.assertEqual(self.order.total_amount, 600)
        # Advance 200 -> balance = 400
        self.assertEqual(self.order.balance, 400)
        # Partial payment
        self.assertEqual(self.order.payment_status, "partial")
        # Profit margin = (200 - 120) * 3 = 240
        self.assertEqual(self.order.estimated_profit, 240)
        self.assertTrue(self.order.is_active)

    def test_dashboard_view(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Press")
        self.assertContains(response, "500 Cards Order")

    def test_order_status_update_ajax(self):
        response = self.client.post(
            reverse("order_update_status", kwargs={"pk": self.order.id}),
            {"status": "ready"},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, "ready")

    def test_order_invoice_view(self):
        response = self.client.get(reverse("order_invoice", kwargs={"pk": self.order.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "JOB ESTIMATE / INVOICE")
        self.assertContains(response, "Acme Corp")

    def test_order_export_csv(self):
        response = self.client.get(reverse("order_export_csv"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn(b"Visiting Cards", response.content)

    def test_customer_creation_ajax(self):
        response = self.client.post(
            reverse("customer_create") + "?format=json",
            {
                "name": "Beta School",
                "mobile_no": "8887776665",
                "email": "beta@example.com",
                "address": "Noida",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Customer.objects.filter(name="Beta School", owner=self.owner).exists())

    def test_product_creation_ajax(self):
        response = self.client.post(
            reverse("product_create") + "?format=json",
            {
                "name": "Brochure A4",
                "price": "45",
                "cost_price": "25",
                "stocks": "500",
            },
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Product.objects.filter(name="Brochure A4", owner=self.owner).exists())

    def test_all_routes_accessible(self):
        routes_to_test = [
            ("root", {}, 302),
            ("dashboard", {}, 200),
            ("order_list", {}, 200),
            ("order_create", {}, 200),
            ("order_edit", {"pk": self.order.id}, 200),
            ("order_delete", {"pk": self.order.id}, 200),
            ("order_invoice", {"pk": self.order.id}, 200),
            ("order_export_csv", {}, 200),
            ("customer_list", {}, 200),
            ("customer_create", {}, 200),
            ("customer_edit", {"pk": self.customer.id}, 200),
            ("customer_delete", {"pk": self.customer.id}, 200),
            ("product_list", {}, 200),
            ("product_create", {}, 200),
            ("product_edit", {"pk": self.product.id}, 200),
            ("product_delete", {"pk": self.product.id}, 200),
            ("profile", {}, 200),
            ("login", {}, 200),
        ]

        for route_name, kwargs, expected_status in routes_to_test:
            url = reverse(route_name, kwargs=kwargs) if kwargs else reverse(route_name)
            response = self.client.get(url)
            self.assertEqual(
                response.status_code,
                expected_status,
                f"Route '{route_name}' ({url}) returned status {response.status_code}, expected {expected_status}",
            )


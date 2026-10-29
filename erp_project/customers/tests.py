import csv
import io

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from users.models import Role, User, UserRole
from .models import Customer


class CustomerBulkCreateTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='customer-admin', password='password')
        role = Role.objects.create(role_name='Customer admin', customers=2)
        UserRole.objects.create(user=self.user, role=role)
        self.client.force_login(self.user)

    def test_upload_accepts_quoted_multiline_fields(self):
        headers = [
            'id_customer', 'legal_name', 'name', 'tax_id', 'country', 'state_province',
            'city', 'address', 'zip_code', 'phone', 'email', 'contact_name',
            'contact_role', 'category', 'payment_terms', 'currency', 'payment_method',
            'bank_account', 'status',
        ]
        row = [
            'C-001', 'Example LLC', 'Example Customer', 'T-001', 'Country', 'State',
            'City', 'Line 1\nLine 2', '12345', '1234567890', 'customer@example.com',
            'Contact Person', 'Manager', 'Retail', 'Net 30', 'USD', 'Wire',
            'Account 1', 'Active',
        ]
        csv_content = io.StringIO(newline='')
        writer = csv.writer(csv_content)
        writer.writerow(headers)
        writer.writerow(row)
        upload = SimpleUploadedFile('customers.csv', csv_content.getvalue().encode('utf-8'), content_type='text/csv')

        response = self.client.post(reverse('customers:customer_bulk_create'), {'csv_file': upload})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['successful_count'], 1)
        self.assertEqual(Customer.objects.get(id_customer='C-001').address, 'Line 1\nLine 2')

    def test_upload_accepts_semicolon_delimited_csv(self):
        headers = [
            'id_customer', 'legal_name', 'name', 'tax_id', 'country', 'state_province',
            'city', 'address', 'zip_code', 'phone', 'email', 'contact_name',
            'contact_role', 'category', 'payment_terms', 'currency', 'payment_method',
            'bank_account', 'status',
        ]
        row = [
            'C-002', 'Example LLC', 'Example Customer', 'T-002', 'Country', 'State',
            'City', 'Address', '12345', '1234567890', 'customer@example.com',
            'Contact Person', 'Manager', 'Retail', 'Net 30', 'USD', 'Wire',
            'Account 1', 'Active',
        ]
        csv_content = io.StringIO(newline='')
        writer = csv.writer(csv_content, delimiter=';')
        writer.writerow(headers)
        writer.writerow(row)
        upload = SimpleUploadedFile('customers.csv', csv_content.getvalue().encode('utf-8'), content_type='text/csv')

        response = self.client.post(reverse('customers:customer_bulk_create'), {'csv_file': upload})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['successful_count'], 1)
        self.assertTrue(Customer.objects.filter(id_customer='C-002').exists())

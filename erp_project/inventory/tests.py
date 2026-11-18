from django.test import SimpleTestCase
from django.urls import resolve


class InventoryBulkUploadUrlTests(SimpleTestCase):
    def test_bulk_upload_url_resolves_to_view(self):
        match = resolve('/bulk-upload/', urlconf='inventory.urls')

        self.assertEqual(match.func.__name__, 'inventory_bulk_upload')

from django.test import TestCase
from django.contrib.auth.models import User
from .models import Bookmark, Tag
import unittest

class BookmarkTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.tag = Tag.objects.create(creator=self.user, title='Test Tag')
        self.bookmark_data = {
            'user': self.user,
            'url': 'https://example.com',
            'description': 'Example description',
            'title': 'Example Bookmark',
        }

    def test_create_bookmark(self):
        bookmark = Bookmark.objects.create(**self.bookmark_data)
        self.assertEqual(bookmark.user, self.user)
        self.assertEqual(bookmark.url, 'https://example.com')
        self.assertEqual(bookmark.description, 'Example description')
        self.assertEqual(bookmark.title, 'Example Bookmark')

    def test_update_bookmark(self):
        bookmark = Bookmark.objects.create(**self.bookmark_data)
        updated_data = {
            'url': 'https://updated-example.com',
            'description': 'Updated description',
            'title': 'Updated Bookmark',
        }
        bookmark.url = updated_data['url']
        bookmark.description = updated_data['description']
        bookmark.title = updated_data['title']
        bookmark.save()

        updated_bookmark = Bookmark.objects.get(pk=bookmark.pk)
        self.assertEqual(updated_bookmark.url, 'https://updated-example.com')
        self.assertEqual(updated_bookmark.description, 'Updated description')
        self.assertEqual(updated_bookmark.title, 'Updated Bookmark')

if __name__ == '__main__':
    unittest.main()

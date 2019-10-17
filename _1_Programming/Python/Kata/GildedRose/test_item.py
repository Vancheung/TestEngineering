from unittest import TestCase

from kata.Item import Item, Backstage


class TestItem(TestCase):
    def test_update_item(self):
        item = Backstage(sell_in=11, quality=20)
        item.update_item()
        self.assertEqual(item.quality, 21)
        item.update_item()
        self.assertEqual(item.quality, 23)

from unittest import TestCase, main

from kata.gilded_rose import GildedRose
from kata.Item import Item


class TestGildedRose(TestCase):
    def test_update_quality(self):
        items = [Item("foo", 0, 0)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEquals("foo", items[0].name)




if __name__ == '__main__':
    main()

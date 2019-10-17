# -*- coding: utf-8 -*-
from __future__ import print_function

from kata.gilded_rose import GildedRose
from kata.Item import Item, Backstage, AgedBrie, Sulfuras
import sys


def main():
    with open('out.txt', 'w') as f_handler:
        sys.stdout = f_handler
        print("OMGHAI!")
        items = [
            Item(name="+5 Dexterity Vest", sell_in=10,
                               quality=20),
            AgedBrie(sell_in=2, quality=0),
            Item(name="Elixir of the Mongoose", sell_in=5,
                               quality=7),
            Sulfuras(sell_in=0, quality=80),
            Sulfuras(sell_in=-1, quality=80),
            Backstage(sell_in=15, quality=20),
            Backstage(sell_in=10, quality=49),
            Backstage(sell_in=5, quality=49),
            Item(name="Conjured Mana Cake", sell_in=3, quality=6),
            # <-- :O
        ]
        days = 2

        for day in range(days):
            print("-------- day %s --------" % day)
            print("name, sellIn, quality")
            for item in items:
                print(item)
            print("")
            GildedRose(items).update_quality()


if __name__ == "__main__":
    main()

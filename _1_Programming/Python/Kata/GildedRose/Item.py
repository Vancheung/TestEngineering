class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)

    def update_item(self):
        self.sell_in_pass_one_day()
        self.update_item_quantities()
        if self.is_expired():
            self.update_after_expired()

    def update_after_expired(self):
        self.quality_minus_one()

    def update_item_quantities(self):
        self.quality_minus_one()

    def is_expired(self):
        return self.sell_in < 0

    def sell_in_pass_one_day(self):
        self.sell_in = self.sell_in - 1

    def quality_minus_one(self):
        if self.quality > 0:
            self.quality = self.quality - 1

    def quality_plus_one(self):
        if self.quality < 50:
            self.quality = self.quality + 1


class Backstage(Item):
    def __init__(self, sell_in, quality):
        Item.__init__(self, "Backstage passes to a TAFKAL80ETC concert",
                      sell_in, quality)

    def update_after_expired(self):
        self.quality = 0

    def update_item_quantities(self):
        self.quality_plus_one()
        if self.sell_in < 10:
            self.quality_plus_one()
        if self.sell_in < 5:
            self.quality_plus_one()


class AgedBrie(Item):
    def __init__(self, sell_in, quality):
        Item.__init__(self, "Aged Brie", sell_in, quality)

    def update_after_expired(self):
        self.quality_plus_one()

    def update_item_quantities(self):
        self.quality_plus_one()


class Sulfuras(Item):
    def __init__(self, sell_in, quality):
        Item.__init__(self, "Sulfuras, Hand of Ragnaros", sell_in, quality)

    def update_after_expired(self):
        pass

    def update_item_quantities(self):
        pass

    def sell_in_pass_one_day(self):
        pass

from cachetools import TTLCache


class BookCache(TTLCache):
    def popitem(self):
        key, value = super().popitem()
        value.save_to_file()
        return key, value

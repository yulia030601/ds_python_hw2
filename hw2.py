import json
import keyword
from collections import abc


class ColorizeMixin:
    """ Adds color to print(object) """
    repr_color_code = 32  # default colour, can be changed in Advert

    def __str__(self):
        return f'\033[1;{self.repr_color_code}m {repr(self)}'


class Unpacker:
    """ Converts dictionary to attributes when they are called """

    def __init__(self, mapping):
        self._mapping = {}
        for key, val in mapping.items():
            if keyword.iskeyword(key):
                self._mapping[key + '_'] = val
            elif key == 'price':
                self._mapping['_' + key] = val
            else:
                self._mapping[key] = val

    def __getattr__(self, item):
        if hasattr(self._mapping, item):
            return getattr(self._mapping, item)
        else:
            if isinstance(self._mapping[item], abc.Mapping):
                return Unpacker(self._mapping[item])  # recursively get attributes to transform "location"
            else:
                return self._mapping[item]


class Advert(ColorizeMixin, Unpacker):
    """ Enables interaction with json-advertisement """
    repr_color_code = 33

    def __init__(self, mapping):
        super().__init__(mapping)  # dynamically gets attributes via Unpacker
        self._price = self.price

    @property
    def price(self):
        try:
            self._price
        except:
            return 0
        else:
            if self._price < 0:
                raise ValueError('must be >= 0')
            else:
                return self._price

    def __repr__(self) -> str:
        return f'{self.title} | {self.price} ₽'

from models_.exceptions import WrongInstanceError


class BaseProduct:
    def __init__(self, name, artist, price, product_type):
        self.name = name
        self.artist = artist
        self.price = price
        self.product_type = product_type

    def __str__(self):
        return f'{self.name}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return all((
                self.name == other.name,
                self.artist == other.artist
            ))
        else:
            raise WrongInstanceError(
                f'Wrong compared object. Expected instance: {self.__class__}.'
            )

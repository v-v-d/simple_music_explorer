from models.exceptions import WrongInstanceError


class BaseUser:
    def __init__(self, name, email, is_active=True):
        self.name = name
        self.email = email
        self.is_active = is_active

    def __str__(self):
        return f'{self.name}'

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.email == other.email
        else:
            raise WrongInstanceError(
                f'Wrong compared object. Expected instance: {self.__class__}.'
            )


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

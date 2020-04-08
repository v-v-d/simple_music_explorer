from pytest import fixture

from models_.mixins import PrototypeMixin


@fixture()
def original_fixture():
    class Original(PrototypeMixin):
        def __init__(self, a, b):
            self.a = a
            self.b = b

        def summ(self):
            return self.a + self.b

    return Original(1, 2)


def test_prototype_mixin(original_fixture):
    prototype = original_fixture.clone()
    assert all((
        original_fixture.a == prototype.a,
        original_fixture.b == prototype.b,
        original_fixture.summ() == prototype.summ(),
    ))

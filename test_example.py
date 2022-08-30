from python_cicd import add, sub


def test_add():
    assert add.add(1, 1) == 2


def test_sub():
    assert sub.sub(1, 1) == 0

from pydplace import API


def test_data():
    api = API('.')
    assert api.check()


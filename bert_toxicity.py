
from detoxify import Detoxify


def check_text(text):
    results = Detoxify('multilingual').predict([text])
    return results
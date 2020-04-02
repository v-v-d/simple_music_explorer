from abc import ABC, abstractmethod


class AbstractController(ABC):
    def __init__(self, request):
        self.request = request

    @abstractmethod
    def make_response(self, data, code):
        pass

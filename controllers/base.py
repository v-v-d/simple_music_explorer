from controllers.interfaces import AbstractController


class BaseController(AbstractController):
    def make_response(self, data, code):
        return {
            'action': self.request.get('action'),
            'time': self.request.get('time'),
            'data': data,
            'code': code,
        }

    def validate_request(self, *attrs):
        message = 'Attribute is required'
        return {attr: message for attr in attrs if attr not in self.request}

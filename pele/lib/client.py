from builtins import object
import json, requests, time


class PeleRequests(object):
    def __init__(self, base_url):
        self.session = requests.session()
        self.base_url = base_url 
        self.token = None
        self._set_token()

    def _set_token(self):
        r = self.session.post(self.base_url + '/login')
        if r.status_code == 429 and 'Retry-After' in r.headers:
            sleep_time = float(r.headers['Retry-After'])
            print("hit rate limit. sleeping for {} seconds".format(sleep_time))
            time.sleep(sleep_time)
            r = self.session.post(self.base_url + '/login')
        r.raise_for_status()
        self.token = r.json()['token']

    def _decorator(f):
        def wrapper(self, *args, **kargs):
            if 'X-API-KEY' not in kargs.get('headers', {}):
                kargs.setdefault('headers', {})['X-API-KEY'] = self.token
            r = f(self, *args, **kargs)
            if r.status_code == 401:
                self._set_token() # refresh token
                kargs['headers']['X-API-KEY'] = self.token
                r = f(self, *args, **kargs)
            return r
        return wrapper

    @_decorator
    def request(self, *args, **kargs):
        return self.session.request(*args, **kargs)

    @_decorator
    def head(self, *args, **kargs):
        return self.session.head(*args, **kargs)

    @_decorator
    def get(self, *args, **kargs):
        return self.session.get(*args, **kargs)

    @_decorator
    def post(self, *args, **kargs):
        return self.session.post(*args, **kargs)

    @_decorator
    def put(self, *args, **kargs):
        return self.session.put(*args, **kargs)

    @_decorator
    def patch(self, *args, **kargs):
        return self.session.patch(*args, **kargs)

    @_decorator
    def delete(self, *args, **kargs):
        return self.session.delete(*args, **kargs)

    _decorator = staticmethod(_decorator)

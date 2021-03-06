from builtins import object
import requests
import time


class PeleRequests(object):
    def __init__(self, base_url, verify=True, auth=True):
        """
        :param base_url: Pele's Rest API base endpoint
        :param verify: verify requests with SSL certs
        :param auth: (boolean) authenticate requests (set to True if Pele's Rest API server is authenticated)
        """
        self.auth = auth
        self.session = requests.session()
        self.base_url = base_url 
        self.verify = verify 
        self.token = None
        if self.auth:
            self._set_token()

    def _set_token(self):
        r = self.session.post(self.base_url + '/login', verify=self.verify)
        if r.status_code == 429 and 'Retry-After' in r.headers:
            sleep_time = float(r.headers['Retry-After'])
            print("hit rate limit. sleeping for {} seconds".format(sleep_time))
            time.sleep(sleep_time)
            r = self.session.post(self.base_url + '/login', verify=self.verify)
        r.raise_for_status()
        self.token = r.json()['token']

    def _decorator(f):
        def wrapper(self, *args, **kwargs):
            if 'verify' not in kwargs:
                kwargs['verify'] = self.verify
            if self.auth is False:
                r = f(self, *args, **kwargs)
            else:
                if 'X-API-KEY' not in kwargs.get('headers', {}):
                    kwargs.setdefault('headers', {})['X-API-KEY'] = self.token
                r = f(self, *args, **kwargs)
                if r.status_code == 401:
                    self._set_token()  # refresh token
                    kwargs['headers']['X-API-KEY'] = self.token
                    r = f(self, *args, **kwargs)
            return r
        return wrapper

    @_decorator
    def request(self, *args, **kwargs):
        return self.session.request(*args, **kwargs)

    @_decorator
    def head(self, *args, **kwargs):
        return self.session.head(*args, **kwargs)

    @_decorator
    def get(self, *args, **kwargs):
        return self.session.get(*args, **kwargs)

    @_decorator
    def post(self, *args, **kwargs):
        return self.session.post(*args, **kwargs)

    @_decorator
    def put(self, *args, **kwargs):
        return self.session.put(*args, **kwargs)

    @_decorator
    def patch(self, *args, **kwargs):
        return self.session.patch(*args, **kwargs)

    @_decorator
    def delete(self, *args, **kwargs):
        return self.session.delete(*args, **kwargs)

    _decorator = staticmethod(_decorator)

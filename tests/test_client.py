from pele.lib.client import PeleRequests
import time

    
base_url = "http://localhost:8877/api/v0.1"

pr = PeleRequests(base_url)
while True:
    #r = pr.request('get', base_url + '/test/echo', params={'echo_str': 'asdfasdf'})
    r = pr.get(base_url + '/test/echo', params={'echo_str': 'asdfasdf'})
    print("status_code: {}".format(r.status_code))
    print("content: {}".format(r.content))
    print("content: {}".format(r.headers))
    #print("json: {}".format(r.json()))
    time.sleep(2)

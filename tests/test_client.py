from pele.lib.client import PeleRequests
import time

    
base_url = "http://localhost:8877/api/v0.1"

pr = PeleRequests(base_url)
while True:
    # r = pr.request('get', base_url + '/test/echo', params={'echo_str': 'asdfasdf'})
    r = pr.get(base_url + '/test/echo', params={'echo_str': 'asdfasdf'})
    print(f"status_code: {r.status_code}")
    print(f"content: {r.content}")
    print(f"content: {r.headers}")
    # print("json: {}".format(r.json()))
    time.sleep(2)

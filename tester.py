import json
import logging
import urllib
import requests

class Test():
    proxy = None

    def __init__(self, name, url, method="get", kwargs={}, desc=None, custom_check=None):
        self.name = name
        self.desc = desc
        self.url = url
        self.method = method
        self.kwargs = kwargs
        self.custom_check = custom_check or self._check
        self.status = None
        self.error_text = None

    @staticmethod
    def _check(resp):
        text = json.dumps(dict(respText=resp.text))[:50]
        if resp.status_code == 200:
            return 1, text
        else:
            return 0, text

    def run(self):
        if 'timeout' not in self.kwargs:
            self.kwargs['timeout'] = 7.0

        if 'params' not in self.kwargs:
            self.kwargs['params'] = dict()
        self.kwargs['params']['z'] = 'statuscheck'

        try:
            resp = requests.request(self.method, self.url, **self.kwargs)
        except Exception as e:
            self.status = 0
            self.error_text = e
            return

        # Handle checkers
        res = self.custom_check(resp)
        if type(res) in (type(list()), type(tuple())) and len(res) == 2:
            self.status, self.error_text = res
        else:
            self.status = res

        if self.status:
            self.status = 1
        else:
            self.status = 0

        logging.info("URL %s. RESP %s. HEADERS %s", self.url, resp.status_code, resp.headers)
        return resp

    def report(self):
        if not self.status:
            self.run()
        url = "http://trovstature.appspot.com/log/%s/%s" % (urllib.quote(self.name), self.status)
        resp = requests.get(url, params=dict(error_text=self.error_text))
        try:
            resp.raise_for_status()
        except:
            logging.error(resp.text)
            raise


def run_tests():
    def server_header_check(header):
        def f(resp):
            if (resp.status_code == 404 and 'is invalid.' in resp.text):
                # Good so far.
                if resp.headers['trov-hostname'] == header:
                    return 1
            return 0, "Expected header (trov-hostname: %s) not present. Headers(%s)" % (header, resp.headers)
        return f

    tests = (
        Test(name="haproxy", url="http://beta.trov.com/"),
        Test(name="Varda", url="https://personal.trov.com/"),
        #hap-server=oahu03-A
        Test(name="TrovServiceMongo-oahu03-A", url="https://beta.trov.com/Trov.Service/api/v1.0/trovs/invites/trovcomplete",
             method="POST",
             kwargs={
                 "data": '{"inviteToken": "49W8FR","email": "bob.loblaw@lawblog.com","password": "trustno1","phoneNumber": "(555) 867 5309"}',
                 "headers": {"content-type":"application/json", "cookie": "hap-server=oahu03-A", 'trov-client': 'molokini'}
             },
             custom_check=server_header_check('oahu03.lvdc - A')
        ),
        #hap-server=oahu03-B
        Test(name="TrovServiceMongo-oahu03-B", url="https://beta.trov.com/Trov.Service/api/v1.0/trovs/invites/trovcomplete",
             method="POST",
             kwargs={
                 "data": '{"inviteToken": "49W8FR","email": "bob.loblaw@lawblog.com","password": "trustno1","phoneNumber": "(555) 867 5309"}',
                 "headers": {"content-type":"application/json", "cookie": "hap-server=oahu03-B", 'trov-client': 'molokini'}
             },
             custom_check=server_header_check('oahu03.lvdc - B')
        ),
        #hap-server=oahu04-A
        Test(name="TrovServiceMongo-oahu04-A", url="https://beta.trov.com/Trov.Service/api/v1.0/trovs/invites/trovcomplete",
             method="POST",
             kwargs={
                 "data": '{"inviteToken": "49W8FR","email": "bob.loblaw@lawblog.com","password": "trustno1","phoneNumber": "(555) 867 5309"}',
                 "headers": {"content-type":"application/json", "cookie": "hap-server=oahu04-A", 'trov-client': 'molokini'}
             },
             custom_check=server_header_check('oahu04.lvdc - A')
        ),
        #hap-server=oahu04-B
        Test(name="TrovServiceMongo-oahu04-B", url="https://beta.trov.com/Trov.Service/api/v1.0/trovs/invites/trovcomplete",
             method="POST",
             kwargs={
                 "data": '{"inviteToken": "49W8FR","email": "bob.loblaw@lawblog.com","password": "trustno1","phoneNumber": "(555) 867 5309"}',
                 "headers": {"content-type":"application/json", "cookie": "hap-server=oahu04-B", 'trov-client': 'molokini'}
             },
             custom_check=server_header_check('oahu04.lvdc - B')
        ),
        Test(name="google!", url="http://www.google.com/"),
        Test(name="Status500", url="http://httpbin.org/status/500"),
    )
    for test in tests:
        test.report()


if __name__ == "__main__":

    # logging.basicConfig(level='INFO')
    # run_tests()
    t = Test(name="haproxy", url="http://httpbin.org/get").run()
    print t.text
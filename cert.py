from webapp2 import *

class LetsEncryptHandler(RequestHandler):

    def get(self, challenge):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('ME-cbDcQdemUHVievxTI_XfW6LBHKZ2E4v0aeewk1lA.UYWdktLXsGzSHhuUf5CRC-Hlu7NoHtUS2jOJL2NfQ48')
application = WSGIApplication([
    ('/.well-known/acme-challenge/([\w-]+)', LetsEncryptHandler),
])

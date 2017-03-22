from google.appengine.ext import webapp

class LetsEncryptHandler(webapp.RequestHandler):

    def get(self, challenge):
        self.response.headers['Content-Type'] = 'text/plain'
        responses = {
                    '[challenge 1]': '[response 1]',
                    '[challenge 2]': '[response 2]'
                }
        self.response.write(responses.get(challenge, ''))

application = webapp.WSGIApplication([
    ('/.well-known/acme-challenge/([\w-]+)', LetsEncryptHandler),
])

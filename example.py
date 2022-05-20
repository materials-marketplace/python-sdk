"""Simple script illustrating some of the features of this package."""
from pprint import pprint

from marketplace import MarketPlaceApp
from marketplace.client import Client

# General MarketPlaceClient for simple requests like user info
# Remember to save your access token in an environment variable with
# export MP_ACCESS_TOKEN="<token>"
mp_client = Client()
# Show the user information
pprint(mp_client.userinfo())


# To simply instantiate a MarketPlaceApp with a client id
app = MarketPlaceApp(application_id="<application_id>")
app.healthy()

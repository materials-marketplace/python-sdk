"""Simple script illustrating some of the features of this package."""
from pprint import pprint

from marketplace.app.marketplace_app import MarketPlaceApp
from marketplace.client import Client

# General MarketPlaceClient for simple requests like user info
# Remember to save your access token in an environment variable with
# export MP_ACCESS_TOKEN="<token>"
mp_client = Client()
# Show the user information
pprint(mp_client.userinfo)


# To simply instantiate a MarketPlaceApp with a client id
mp = MarketPlaceApp(client_id="<application_client_id>")
print(mp.heartbeat())


# To extend the MarketPlaceApp with custom implementations
class MyMarketPlaceApp(MarketPlaceApp):
    def heartbeat(self) -> str:
        res = super().heartbeat()
        return f"heartbeat response: {res}"


my_mp_app = MyMarketPlaceApp(client_id="<application_client_id>")
print(my_mp_app.heartbeat())

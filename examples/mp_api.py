"""Simple script illustrating some of the features of this package."""
from pprint import pprint

from fastapi.responses import HTMLResponse

from marketplace.app import get_app
from marketplace.app.v0 import MarketPlaceApp
from marketplace.app.v0_0_1 import MarketPlaceApp as MarketPlaceApp_v_0_0_1
from marketplace.client import MarketPlaceClient

# General MarketPlaceClient for simple requests like user info
# Remember to save your access token in an environment variable with
# export MP_ACCESS_TOKEN="<token>"
mp_client = MarketPlaceClient()
# Show the user information
pprint(mp_client.userinfo)


# To simply instantiate a MarketPlaceApp with a client id
mp = get_app(app_id="<application_client_id>")
print(mp.heartbeat())


# To extend the MarketPlaceApp with custom implementations
class MyMarketPlaceApp(MarketPlaceApp):
    def heartbeat(self) -> HTMLResponse:
        res = super().heartbeat()
        return f"heartbeat response: {res}"


my_mp_app = MyMarketPlaceApp(app_id="<application_client_id>")
print(my_mp_app.heartbeat())


# To extend the MarketPlaceApp with custom implementations for deprecated api version 0.0.1
class MyMarketPlaceApp_v_0_0_1(MarketPlaceApp_v_0_0_1):
    def heartbeat(self) -> str:
        res = super().heartbeat()
        return f"heartbeat response: {res}"


my_mp_app_v_0_0_1 = MyMarketPlaceApp_v_0_0_1(client_id="<application_client_id>")
print(my_mp_app_v_0_0_1.heartbeat())

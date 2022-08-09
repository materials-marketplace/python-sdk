class _MarketPlaceAppBase:
    def __init__(self, client, app_id):
        self._client = client
        self.app_id = app_id

        # self._capabilities = self._client.get_app_capabilities(self.app_id)  # TODO
        self._capabilities = ["listCollections"]  # FOR DEBUGGING

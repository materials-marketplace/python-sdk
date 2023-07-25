from marketplace.data_sink_client.session import MPSession

with MPSession() as test:
    objects = test.list_collections()
    print(objects)

from marketplace.data_sink_client.session import MPSession

with MPSession() as test:
    objects = test.list_datasets(collection_name="c1")
    print(objects)

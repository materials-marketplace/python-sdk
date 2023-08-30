from marketplace.data_sink_client.session import MPSession

with MPSession() as test:
    objects = test.delete_dataset(collection_name="c1", dataset_name="d1")
    print(objects)

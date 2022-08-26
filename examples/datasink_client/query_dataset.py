from marketplace.data_sink_client.session import MPSession

query = "SELECT ?subject ?predicate ?object WHERE {{ ?subject ?predicate ?object . }} LIMIT 5"
with MPSession() as test:
    objects = test.query_dataset(collection_name="c1", dataset_name="d1", query=query)
    print(objects)

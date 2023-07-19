from marketplace.data_sink_client.session import MPSession

query = """SELECT ?subject ?predicate ?object WHERE {{ ?subject ?predicate ?object . }} LIMIT 5"""
with MPSession() as test:
    objects = test.query(query=query)
    print(objects)

from marketplace.datasink_client.session import MPSession

marketplace_url = "https://materials-marketplace.eu/"
access_token = "PASTE_TOKEN_HERE"
client_id = "edb56699-9377-4f41-b1c7-ef2f46dac707"

query = """SELECT ?subject ?predicate ?object WHERE {{ ?subject ?predicate ?object . }} LIMIT 5"""
with MPSession(
    marketplace_host_url=marketplace_url, access_token=access_token, client_id=client_id
) as test:
    objects = test.query_dataset(
        collection_name="c1", dataset_name="data_test", query=query
    )
    print(objects)

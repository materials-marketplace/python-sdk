from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.get_collection_dcat(collection_name="c1")
    print(objects)

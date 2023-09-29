from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.delete_collection(collection_name="c1")
    print(objects)

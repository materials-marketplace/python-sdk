from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.list_collections()
    print(objects)

from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.get_dataset_dcat(collection_name="c1", dataset_name="d1")
    print(objects)

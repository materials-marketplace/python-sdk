from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.download_datasets_from_collection(
        collection_name="Simulation_folder9",
        targetdir="/root/symphony/reaxpro",
        raise_if_directory_not_empty=False,
    )
    print(objects)

from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.create_dataset_from_path(
        path="/root/symphony/reaxpro/Simulation_folder9/file3.txt",
        collection_name="ams_wrapper9",
    )
    print(objects)

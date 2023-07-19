from marketplace.data_sink_client.session import MPSession

with MPSession() as test:
    objects = test.create_datasets_from_sourcedir(
        sourcedir="/root/symphony/reaxpro/Simulation_folder9",
        collection_name="Simulation_folder1",
    )
    print(objects)

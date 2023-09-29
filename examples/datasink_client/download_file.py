from marketplace.datasink_client.session import MPSession

with MPSession() as test:
    objects = test.download_dataset(
        collection_name="upload_file_example",
        dataset_name="file3.txt",
        targetdir="/root/symphony/reaxpro",
        raise_if_directory_not_empty=False,
    )
    print(objects)

import os
import os.path
from functools import wraps

# from dotenv import find_dotenv, load_dotenv
from keycloak import KeycloakOpenID

from marketplace.app import MarketPlaceClient, get_app
from marketplace.datasink_client.utils import (
    get_collections_from_catalog,
    parse_objects_from_collection,
)


def reconfigure_if_expired(func):
    @wraps(func)
    def func_(self, *arg, **kwargs):
        try:
            r = func(self, *arg, **kwargs)
            return r
        except Exception as e:
            print(
                "API encountered exception. Please check if all your environment variables configured properly once. Error details: ",
                str(e),
            )
            # temporary work around to catch Un Authorized error
            """error = str(e)
            if len(error.split("401 Unauthorized")) > 0:
                print("Token expired. Reconfiguring again.")
                token = configure()
                os.environ["MP_ACCESS_TOKEN"] = token
                r = func(self, *arg, **kwargs)
                return r
            else:
                raise RuntimeError(e)"""

    return func_


def configure():
    # Configure client
    server_url = os.environ.get("KEYCLOAK_SERVER_URL")
    client_id = os.environ.get("KEYCLOAK_CLIENT_ID")
    realm_name = os.environ.get("KEYCLOAK_REALM_NAME")
    client_key = os.environ.get("KEYCLOAK_CLIENT_SECRET_KEY")
    user = os.environ.get("MARKETPLACE_USERNAME")
    passwd = os.environ.get("MARKETPLACE_PASSWORD")
    keycloak_openid = KeycloakOpenID(
        server_url=server_url,
        client_id=client_id,
        realm_name=realm_name,
        client_secret_key=client_key,
    )
    token = keycloak_openid.token(user, passwd)
    token = token["access_token"]
    return token


class MPSession:
    """ReaxPro-MarketPlace Session API Wrapper.

    This session wrapper simplifies generic tasks.

    Keyword arguments:
    :param token: necessary token for acessing a MarketPlace registered Datasink

    """

    @reconfigure_if_expired
    def __init__(
        self, marketplace_host_url=None, access_token=None, client_id=None, **kwargs
    ):
        CLIENT_ID = client_id or os.environ.get("CLIENT_ID")
        # configure()
        mp_client = MarketPlaceClient(
            marketplace_host_url=marketplace_host_url, access_token=access_token
        )
        self.marketPlace = get_app(app_id=CLIENT_ID, client=mp_client)

    @reconfigure_if_expired
    def create_dataset(
        self, collection_name, dataset_name, sub_collection_id, abs_path
    ):
        """create a dataset to the MarketPlace DataSink.

        Keyword arguments:
        :param collection_name: A string value which indicates the title of the catalog the dataset belongs to.
        :param dataset_name: A string value which indicates the title of the dataset/dataset.
        :param sub_collection_id: A string representing ID of sub catalog(catalog within a catalog) to which this dataset belong to.

        :return status
        """
        try:
            with open(abs_path, "rb") as f:
                file_content = f.read()

            if not file_content:
                raise Exception("Empty file content in ", abs_path)

            config = {
                "sub_collection_id": sub_collection_id,
            }

            files = {
                "file": (dataset_name, file_content),
            }
            response = self.marketPlace.create_dataset(
                collection_name, dataset_name, config=config, file=files
            )
            if "dataset_id" not in response:
                print(response)
                return None
            else:
                return response["dataset_id"]

        except Exception as e:
            print(
                f"Something went wrong while uploading the data from {abs_path}. "
                + str(e)
            )
            return None

    @reconfigure_if_expired
    def create_collection(self, collection_name, sub_collection_id):
        """create collection/catalog to the MarketPlace DataSink.

        Keyword arguments:
        :param collection_name: A string value which indicates the title of the collection/catalog.
        :param sub_collection_id: A string value which indicates the ID of the collection to add this collection/catalog to.

        :return response
        """

        try:
            config = {"sub_collection_id": sub_collection_id}

            response = self.marketPlace.create_collection(
                collection_name=collection_name, config=config
            )
            if "collection_id" not in response:
                #print(response)
                return None
            else:
                return response["collection_id"]

        except Exception as e:
            #print(
            #    f"Something went wrong while uploading the data with title {collection_name}. "
            #    + str(e)
            #)
            return None

    @reconfigure_if_expired
    def get_dataset(self, collection_name=None, dataset_name=None):
        """Get binary data from a get request

        :param collection_name: Name of the collection.
        :param dataset_name: Name of the dataset.

        :returns: binary content data stored within the dataset
        """
        response = self.marketPlace.get_dataset(
            collection_name=collection_name, dataset_name=dataset_name
        )

        return response

    @reconfigure_if_expired
    def get_collection_dcat(self, collection_name=None):
        """Get a collection/catalog object from a get request

        :param collection_name: Name of the collection.

        :returns: dcat meta-data for the catalog
        """
        response = self.marketPlace.get_collection_metadata_dcat(
            collection_name=collection_name
        )
        return response

    @reconfigure_if_expired
    def get_dataset_dcat(self, collection_name=None, dataset_name=None):
        """Get a dataset dcat object from a get request

        :param collection_name: Name of the collection.
        :param daatset_name: Name of the dataset.

        :returns: dcat meta-data for the dataset
        """
        response = self.marketPlace.get_dataset_metadata_dcat(
            collection_name=collection_name, dataset_name=dataset_name
        )
        return response

    @reconfigure_if_expired
    def list_collections(self):
        """Returns list of Collections.

        :returns: Dictionary with list of collections
        """
        response = self.marketPlace.list_collections()
        return response

    @reconfigure_if_expired
    def list_datasets(self, collection_name):
        """Returns list of datasets for a specific collection.

        :param collection_name: Name of the collection

        :returns: Dictionary with list of datasets
        """
        response = self.marketPlace.list_datasets(collection_name)
        return response

    @reconfigure_if_expired
    def delete_collection(self, collection_name):
        """Delete a collection from datasink.

        :param collection_name: Name of the collection

        :returns: None on success
        """
        response = self.marketPlace.delete_collection(collection_name)
        return response

    @reconfigure_if_expired
    def delete_dataset(self, collection_name, dataset_name):
        """Delete a dataset from datasink.

        :param collection_name: Name of the collection
        :param dataset_name: Name of the dataset

        :returns: None on success
        """
        response = self.marketPlace.delete_dataset(collection_name, dataset_name)
        return response

    @reconfigure_if_expired
    def query_dataset(self, collection_name, dataset_name, query):
        """Execute a aparql query on a dataset stored in datasink.

        :param collection_name: Name of the collection
        :param dataset_name: Name of the
        :param query: SPARQL query

        :returns: List of data
        """
        response = self.marketPlace.query_dataset(collection_name, dataset_name, query)
        return response

    @reconfigure_if_expired
    def query(self, query, meta_data=False):
        """Execute a aparql query on a dataset stored in datasink.

        :param query: SPARQL query
        :param meta_data: Query meta_data instead of actual data.

        :returns: List of data
        """
        response = self.marketPlace.query(query, meta_data=meta_data)
        return response

    @reconfigure_if_expired
    def create_dataset_from_path(self, path, collection_name=None, dataset_name=None):
        if not os.path.exists(path):
            raise Exception("File " + path + " does not exist.")

        if os.path.isdir(path):
            raise Exception("File " + path + " is a directory")

        if dataset_name is None:
            dataset_name = os.path.basename(path)

        # use name of the file if it is not specified. If in case a collection exists already then it will fails with duplicate error
        if collection_name is None:
            collection_name = os.path.basename(path).split(".")[0]

        response = self.create_datasets_from_paths(
            paths=[path], dataset_names=[dataset_name], collection_name=collection_name
        )
        return response

    @reconfigure_if_expired
    def create_datasets_from_paths(self, paths, collection_name, dataset_names):
        """Inject a list of datasets. A single InformationPackage will be created.

        :param paths: List of filepaths to inject.
        :param collection_name: The title of the collection
        :param dataset_names: The titles of the datasets

        :returns: response
        """
        assert len(paths) == len(dataset_names)

        response_list = []
        if collection_name is not None:
            collection_id = self.create_collection(
                collection_name=collection_name, sub_collection_id=None
            )
            if collection_id is not None:
                response_list.append((collection_name, collection_id))
        else:
            raise Exception("collection title cannot be empty.")

        for path, dataset_name in zip(paths, dataset_names):
            dataset_id = self.create_dataset(
                collection_name=collection_name,
                dataset_name=dataset_name,
                sub_collection_id=None,
                abs_path=path,
            )
            response_list.append((path, dataset_id))

        return response_list

    @reconfigure_if_expired
    def create_datasets_from_sourcedir(
        self, sourcedir: str, collection_name: str = None
    ):
        """Inject a datasets from a directory. A single InformationPackage will be created.

        :param sourcedir: The source directory to create
        :param collection_name: The title of the collection

        :returns: response"""

        assert os.path.isdir(sourcedir), "Source directory doesn't exist."

        if collection_name is None:
            collection_name = os.path.basename(sourcedir)

        response_list = []
        if collection_name is None:
            collection_name = os.path.basename(sourcedir)
        collection_id = self.create_collection(
            collection_name=collection_name, sub_collection_id=None
        )
        if collection_id is None:
            return
        response_list.append((collection_name, collection_id))
        response_list = self.create_objects_from_sourcedir(
            collection_name,
            sourcedir,
            collection_id=collection_id,
            response_list=response_list,
        )

        return response_list

    @reconfigure_if_expired
    def create_objects_from_sourcedir(
        self, collection_name, sourcedir, collection_id, response_list=[]
    ):
        for file in os.listdir(sourcedir):
            if os.path.isdir(os.path.join(sourcedir, file)):
                id = self.create_collection(
                    collection_name=file, sub_collection_id=collection_id
                )
                if id is None:
                    return
                response_list.append((os.path.join(sourcedir, file), id))
                # print("added directory: ", (os.path.join(sourcedir, file), id))
                self.create_objects_from_sourcedir(
                    collection_name, os.path.join(sourcedir, file), id, response_list
                )
            else:
                dataset_id = self.create_dataset(
                    collection_name=collection_name,
                    dataset_name=file,
                    sub_collection_id=collection_id,
                    abs_path=os.path.join(sourcedir, file),
                )
                if dataset_id is None:
                    return
                response_list.append((os.path.join(sourcedir, file), dataset_id))
                # print("added file: ", (os.path.join(sourcedir, file), dataset_id))
        return response_list

    @reconfigure_if_expired
    def download_dataset(
        self,
        collection_name,
        dataset_name,
        targetdir=os.getcwd(),
        raise_if_directory_not_empty=True,
    ):
        """Download the dataset to local directory"""
        result = []
        if not os.path.isdir(targetdir):
            raise Exception("Download Directory" + targetdir + "does not exist.")

        file_path = os.path.join(targetdir, dataset_name)
        content = self.get_dataset(
            collection_name=collection_name, dataset_name=dataset_name
        )
        with open(file_path, "wb") as f:
            f.write(content)
        # print("created file: ", file_path)
        result.append({"download_path": file_path})
        return result

    @reconfigure_if_expired
    def download_datasets_from_search_query(
        self,
        collection_search_query,
        targetdir=os.getcwd(),
        raise_if_directory_not_empty=True,
        raise_if_missing_dataset=True,
        download_mode="digital-object-ids",
        zipfile_name="datasets.zip",
    ):
        """Download the datasets from collections to a local
        directory. Uses a search query as input.

        :param collection_search_query: The collection search query
        :param targetdir: (optional, default=curdir) The directory to download to
        :param raise_if_directory_not_empty: (optional) Raise error when True and directories are not empty
        :param raise_if_missing_dataset: (optional) Raise Exception when trying to download from an empty collection
        :param download_mode: (optional) One of 'digital-object-ids', 'digital-object-titles', 'as-directories', 'as-zipfiles'
        :param zipfile_name: (optional) The optional name of the zipfile

        :returns: tuple(List of paths, List of datasets)

        """
        collections = self.search_collections(
            collection_search_query, include_dataset=False
        )

        # convert collections to python representation
        collections = get_collections_from_catalog(collections)

        result = self.download_datasets_from_collections(
            collections=collections,
            targetdir=targetdir,
            raise_if_directory_not_empty=raise_if_directory_not_empty,
            raise_if_missing_dataset=raise_if_missing_dataset,
            download_mode=download_mode,
        )

        return result

    @reconfigure_if_expired
    def download_datasets_from_collection(
        self,
        collection_name,
        targetdir=os.getcwd(),
        raise_if_directory_not_empty=True,
        download_mode="digital-object-ids",
    ):
        """Download the datasets from collection to a local directory.

        :param collection_name: Name of the collection.
        :param targetdir: (optional, default=curdit) The directory to download to
        :param raise_if_directory_not_empty: (optional) Raise error when True and directories are not empty
        :param download_mode: (optional) TODO: One of 'digital-object-ids', 'digital-object-titles', 'as-directories', 'as-zipfiles'

        :returns: List of (title, file_path, file_type)

        .. note::

           The folder structure as defined in each dataset's `folderPath` will be
           preserved with `targetdir/collection_identifier` as the root directory.

        """

        result = []
        print(targetdir)
        if not os.path.isdir(targetdir):
            raise Exception("Download Directory" + targetdir + "does not exist.")

        if raise_if_directory_not_empty and any(os.listdir(targetdir)):
            raise Exception("Directory " + targetdir + " is not empty.")

        collection = self.get_collection_dcat(collection_name=collection_name)

        # convert to python dictionary. There will be atmost one collection in the list
        packages = parse_objects_from_collection(collection, collection_name, path="")
        # print(packages)

        if len(packages) == 0:
            raise Exception("Error: " + collection)

        for package in packages:
            abs_path = package["path"]
            title = package["title"]
            file_type = package["type"]
            if not os.path.exists(os.path.join(targetdir, abs_path)):
                os.makedirs(os.path.join(targetdir, abs_path))
                # print("created directory: ", os.path.join(targetdir, abs_path))
                result.append((title, os.path.join(targetdir, abs_path), file_type))

            file_path = os.path.join(targetdir, abs_path, title)
            if file_type == "file":
                # print("sending request for, " , collection_identifier, title)
                response = self.get_dataset(
                    collection_name=collection_name, dataset_name=title
                )
                with open(file_path, "wb") as f:
                    f.write(response)
                # print("created file: ", file_path)
                result.append((title, file_path, file_type))

        return result

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        return False

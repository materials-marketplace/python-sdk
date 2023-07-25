import os
import re

from rdflib import Graph


def get_datasets_uid_sparql(collections):
    """A utility that supports searching and retrieving for the datasets uid in a catalog

    Keyword arguments:
    :param collections: response.text

    :return List of datasets uid
    """
    uid_list = []

    g = Graph()
    g.parse(data=collections, format="json-ld")

    qrs = g.query(
        """
        SELECT ?asource ?id
        WHERE {
            ?asource a <http://www.w3.org/ns/dcat#Dataset> .
            ?asource <http://purl.org/dc/terms/identifier> ?id.
            }
        """
    )

    for row in qrs:
        uid_list.append(row.id.value)

    return uid_list


def get_collections_uid_sparql(collections):
    """A utility that supports searching and retrieving for the catalogs uid in a catalog

    Keyword arguments:
    :param collections: response.text

    :return List of catalog objects uid
    """
    uid_list = []

    g = Graph()
    g.parse(data=collections, format="json-ld")

    qrs = g.query(
        """
        SELECT ?asource ?id
        WHERE {
            ?asource a <http://www.w3.org/ns/dcat#Catalog> .
            ?asource <http://purl.org/dc/terms/identifier> ?id.
            }
        """
    )

    for row in qrs:
        uid_list.append(row.id.value)

    return uid_list


def get_collections_from_catalog(collections):
    """A utility that supports converts collections stored as catalog to list of dictionaries.

    Keyword arguments:
    :param collections: response.text

    :return List of dictionary represented collections
    """
    inf_packages = []
    g = Graph()
    g.parse(data=collections, format="json-ld")

    qrs = g.query(
        """
        SELECT ?asource ?identifier ?subject ?title
        WHERE {
            ?asource a <http://www.w3.org/ns/dcat#Catalog> .
            ?asource <http://purl.org/dc/terms/identifier> ?identifier.
            ?asource <http://purl.org/dc/terms/title> ?title.
            }
        """
    )

    for row in qrs:
        inf_packages.append(row.identifier.value)

    return inf_packages


def parse_objects_from_collection(collection, collection_name, path=""):
    """A utility that supports converts collections stored as catalog to list of dictionaries.

    Keyword arguments:
    :param collection: response.text
    :param collection: Name of the collection
    :param path: relative path from root collection

    :return List of dictionary represented collection
    """
    inf_packages = []

    g = Graph()
    g.parse(data=collection, format="json-ld")

    # get all datasets linked to current catalog
    dataset_query = f"""
        SELECT ?catalog_identifier ?catalog_title ?dataset_identifier ?dataset_title
        WHERE {{
            ?asource a <http://www.w3.org/ns/dcat#Catalog> .
            ?asource <http://purl.org/dc/terms/identifier> ?catalog_identifier.
            ?asource <http://purl.org/dc/terms/title> ?catalog_title.
            ?asource <http://www.w3.org/ns/dcat#dataset> ?datasets.
            ?datasets <http://purl.org/dc/terms/identifier> ?dataset_identifier.
            ?datasets <http://www.w3.org/ns/dcat#distribution> ?distribution.
            ?distribution <http://purl.org/dc/terms/title> ?dataset_title
            FILTER regex(?catalog_title, "{collection_name}")
            }}
        """
    qrs = g.query(dataset_query)

    for row in qrs:
        parent_title = row.catalog_title.value
        dataset_title = row.dataset_title.value
        abs_path = os.path.join(path, parent_title)
        inf_packages.append(
            {
                "path": abs_path,
                "title": dataset_title,
                "identifier": row.dataset_identifier.value,
                "type": "file",
            }
        )

    # recursively fetch information of the connected catalog
    catalog_query = f"""
        SELECT ?parent_catalog_identifier ?parent_catalog_title ?catalog_identifier ?catalog_title
        WHERE {{
            ?asource a <http://www.w3.org/ns/dcat#Catalog> .
            ?asource <http://purl.org/dc/terms/identifier> ?parent_catalog_identifier.
            ?asource <http://purl.org/dc/terms/title> ?parent_catalog_title.
            ?asource <http://www.w3.org/ns/dcat#catalog> ?catalogs.
            ?catalogs <http://purl.org/dc/terms/identifier> ?catalog_identifier.
            ?catalogs <http://purl.org/dc/terms/title> ?catalog_title
            FILTER regex(?parent_catalog_title, "{collection_name}")
            }}
        """
    catalogs = g.query(catalog_query)
    for row in catalogs:
        print(row)
        parent_title = row.parent_catalog_title.value
        catalog_title = row.catalog_title.value
        abs_path = os.path.join(path, parent_title, catalog_title)
        updated_path = os.path.join(path, parent_title)
        inf_packages.append(
            {
                "path": abs_path,
                "title": catalog_title,
                "identifier": row.catalog_identifier.value,
                "type": "dir",
            }
        )
        return inf_packages + parse_objects_from_collection(
            collection, catalog_title, path=updated_path
        )

    return inf_packages


def parse_objects_from_datasets(datasets_response):
    """A utility that supports converts datasets  stored as dataset to list of dictionaries.

    Keyword arguments:
    :param datasets_response: response.text

    :return List of dictionary represented digtal objects
    """
    datasets = []

    g = Graph()
    g.parse(data=datasets_response, format="json-ld")

    # get all datasets linked to current catalog
    dataset_query = """
        SELECT ?identifier  ?title
        WHERE {{
            ?asource a <http://www.w3.org/ns/dcat#Dataset> .
            ?asource <http://purl.org/dc/terms/identifier> ?identifier.
            ?asource <http://www.w3.org/ns/dcat#distribution> ?distribution.
            ?distribution <http://purl.org/dc/terms/title> ?title
            }}
        """
    qrs = g.query(dataset_query)

    for row in qrs:
        title = row.title.value
        datasets.append({"title": title, "identifier": row.identifier.value})
    return datasets


def get_datasets_from_catalog(datasets):
    """A utility that supports converts datasets stored as catalog to list of dictionaries.

    Keyword arguments:
    :param datasets: response.text

    :return List of dictionary represented datasets
    """
    dig_objects = []

    g = Graph()
    g.parse(data=datasets, format="turtle")

    qrs = g.query(
        """
        SELECT ?asource ?identifier ?isPartOf ?title ?spatial
        WHERE {
            ?asource a <http://www.w3.org/ns/dcat#Dataset> .
            ?asource <http://purl.org/dc/terms/identifier> ?identifier.
            ?asource <http://purl.org/dc/terms/isPartOf> ?isPartOf.
            ?asource <http://purl.org/dc/terms/title> ?title.
            ?asource <http://purl.org/dc/terms/spatial> ?spatial.
            }
        """
    )

    for row in qrs:
        dataset = {}
        dataset["identifier"] = row.identifier.value
        dataset["isPartOf"] = row.isPartOf.value
        dataset["title"] = row.title.value
        dataset["spatial"] = row.spatial.value
        dig_objects.append(dataset)

    return dig_objects


def get_datasets_uid(collections):
    """An utility function to support search for the datasets.

    Keyword arguments:
    :param collections: collection

    :return List of datasets
    """
    pass


def serialize_jsondl(collections):
    """An utility that enables serializing the response.text into json-ld

    Keyword arguments:
    :param collections: response.text
    :return Collection
    """

    g = Graph().parse(data=collections, format="n3")
    r = g.serialize(format="json-ld")

    return r


def _walk(rootpath, pattern=None, relative_path=".", depth=0, data=[]):
    """Walk root directory and return the absolute paths, the paths relative
    to rootpath and the filenames, optionally matching a regex pattern.

    :param rootpath: (str) The root directory to walk
    :param pattern: (str) the regex pattern for the filenames
    :param depth: int indicates the depth of the folder/file from root directory
    :param data: contains information about all subdirectories and files in theroot path

    :returns: Generator of (absolute_path, relative_to_rootpath_path, filename) tuples.

    """
    absolute_path = os.path.join(rootpath, relative_path)
    for p in os.listdir(absolute_path):
        if os.path.isdir(os.path.join(absolute_path, p)):
            data.append(
                (rootpath, pattern, os.path.join(relative_path, p), depth, True)
            )
            _walk(rootpath, pattern, os.path.join(relative_path, p), depth + 1, data)
            return data
        else:
            if not pattern or (pattern and re.match(pattern, p)):
                data.append(
                    (
                        os.path.join(rootpath, relative_path, p),
                        relative_path,
                        p,
                        depth,
                        False,
                    )
                )

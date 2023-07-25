import ast
import os
import typing as t
from functools import wraps
from pathlib import Path

import click

from marketplace.data_sink_client.session import MPSession


class CommaSeparatedListofPythonLiteralValues(click.Option):
    def type_cast_value(self, ctx, value):
        if value is not None:
            if value.rstrip().endswith(","):
                raise click.BadParameter(value)
            if "," not in value:
                values = [ast.literal_eval(value)]
            else:
                values = [ast.literal_eval(item) for item in value.split(",")]
            return values
        else:
            return None


class CommaSeparatedListofFiles(click.Option):
    def type_cast_value(self, ctx, value):
        if value is not None:
            if value.rstrip().endswith(","):
                raise click.BadParameter(value)
            if "," not in value:
                values = [value]
            else:
                values = value.split(",")
            for item in values:
                if not Path(item).is_file():
                    raise click.BadParameter(f'"{item}" is not a valid file.')
            return values
        else:
            return None


class PythonLiteralOption(click.Option):
    def type_cast_value(self, ctx, value):
        if value is not None:
            try:
                return ast.literal_eval(value)
            except Exception:
                raise click.BadParameter(f'"{value}" is not a valid Python literal.')
        else:
            return None


def mpsession(f):
    @wraps(f)
    # @click.option('--token',type=str,required=True,default='cn389ncoiwuencr', help="Token generated after registration at the MarketPlace")
    def wrapper(*args, **kwargs):
        kwargs.update({"session": MPSession()})

        return f(*args, **kwargs)

    return wrapper


@click.command()
@mpsession
def list_collections(
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.list_collections()
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@mpsession
def list_datasets(
    collection_name: str,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.list_datasets(collection_name=collection_name)
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@mpsession
def get_collection_dcat(
    collection_name: str,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.get_collection_dcat(collection_name=collection_name)
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@click.option(
    "--dataset-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The name of the dataset",
)
@mpsession
def get_dataset_dcat(
    collection_name: str,
    dataset_name: str,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.get_dataset_dcat(
            collection_name=collection_name, dataset_name=dataset_name
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@mpsession
def delete_collection(
    collection_name: str,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.delete_collection(collection_name=collection_name)
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@click.option(
    "--dataset-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The name of the dataset",
)
@mpsession
def delete_dataset(
    collection_name: str,
    dataset_name: str,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.delete_dataset(
            collection_name=collection_name, dataset_name=dataset_name
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--path",
    "-p",
    required=True,
    type=click.STRING,
    help="Absolute or relative path of the file",
)
@click.option(
    "--collection-name",
    "-cn",
    required=False,
    type=click.STRING,
    help="The name of the collection",
)
@click.option(
    "--dataset-name",
    "-dn",
    required=False,
    type=click.STRING,
    help="The name of the dataset",
)
@mpsession
def upload_file_from_path(
    path: str,
    collection_name: t.Optional[str] = None,
    dataset_name: t.Optional[str] = None,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.create_dataset_from_path(
            path=path, collection_name=collection_name, dataset_name=dataset_name
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--path",
    "-p",
    required=True,
    type=click.STRING,
    help="Absolute or relative path of the file",
)
@click.option(
    "--collection-name",
    "-cn",
    required=False,
    type=click.STRING,
    help="The name of the collection",
)
@mpsession
def upload_files_from_folder(
    path: str,
    collection_name: t.Optional[str] = None,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.create_datasets_from_sourcedir(
            sourcedir=path, collection_name=collection_name
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@click.option(
    "--target_dir",
    "-td",
    required=False,
    type=click.STRING,
    help="Absolute or relative path to download",
)
@click.option(
    "--raise_if_directory_not_empty",
    "-r",
    required=False,
    type=click.STRING,
    help="Should the download stop if target dir is not empty",
)
@mpsession
def download_folder(
    collection_name,
    target_dir: t.Optional[str] = None,
    raise_if_directory_not_empty: t.Optional[bool] = False,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        if target_dir is None:
            target_dir = os.getcwd()
        object = session.download_datasets_from_collection(
            targetdir=target_dir,
            collection_name=collection_name,
            raise_if_directory_not_empty=raise_if_directory_not_empty,
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@click.option(
    "--dataset-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The name of the dataset",
)
@click.option(
    "--target_dir",
    "-td",
    required=False,
    type=click.STRING,
    help="Absolute or relative path to download",
)
@click.option(
    "--raise_if_directory_not_empty",
    "-r",
    required=False,
    type=click.STRING,
    help="Should the download stop if target dir is not empty",
)
@mpsession
def download_file(
    collection_name,
    dataset_name,
    target_dir: t.Optional[str] = None,
    raise_if_directory_not_empty: t.Optional[bool] = False,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        if target_dir is None:
            target_dir = os.getcwd()
        object = session.download_dataset(
            targetdir=target_dir,
            collection_name=collection_name,
            dataset_name=dataset_name,
            raise_if_directory_not_empty=raise_if_directory_not_empty,
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--query",
    "-q",
    required=True,
    type=click.STRING,
    help="SPARQL query.",
)
@click.option(
    "--meta-data",
    "-md",
    required=False,
    type=click.BOOL,
    help="whether to executeSPARQL query on meta data.",
)
@mpsession
def query(
    query: str,
    meta_data: str = False,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.query(query=query, meta_data=meta_data)
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")


@click.command()
@click.option(
    "--query",
    "-q",
    required=True,
    type=click.STRING,
    help="SPARQL query.",
)
@click.option(
    "--collection-name",
    "-cn",
    required=True,
    type=click.STRING,
    help="The name of the collection",
)
@click.option(
    "--dataset-name",
    "-dn",
    required=True,
    type=click.STRING,
    help="The name of the dataset",
)
@mpsession
def query_dataset(
    query: str,
    collection_name,
    dataset_name,
    session: t.Optional[MPSession] = None,
) -> int:
    try:
        object = session.query_dataset(
            query=query, collection_name=collection_name, dataset_name=dataset_name
        )
        click.echo(object)
    except Exception as e:
        click.echo(f"{e.__class__.__name__}: {e}")

"""Test the MarkLogic client. The tests are written so that if they pass, they
should leave the database in the same state as before.
"""

from marklogic_client import MarkLogicClient
from uuid import uuid1


def enable_http_logging():
    """Enable low-level HTTP logging to stdout."""
    import logging
    import http.client as http_client
    http_client.HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("requests.packages.urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True


def load_credentials():
    """Load MarkLogic credentials from the .env file."""
    import os
    from dotenv import load_dotenv
    load_dotenv()
    return (
        os.getenv('MARKLOGIC_URL'),
        os.getenv('MARKLOGIC_USERNAME'),
        os.getenv('MARKLOGIC_PASSWORD')
    )


def make_client():
    """Make a MarkLogic client with credentials from the .env file."""
    ml_url, ml_user, ml_pwd = load_credentials()
    return MarkLogicClient(ml_url, ml_user, ml_pwd)


def assert_document_not_found(client, uri):
    """Asserts that there is no document at the given URI, reached by the given
    client.
    """
    response = client.get_document(uri)
    assert response.status_code == 404  # Not Found
    assert not response.ok


def assert_document_found(client, uri):
    """Asserts that there is a document at the given URI, reached by the given
    client.
    """
    response = client.get_document(uri)
    assert response.status_code == 200  # OK
    assert response.ok


def test_xml():
    """Test creating, getting, and deleting of an XML document"""
    enable_http_logging()

    client = make_client()

    # Generate a UUID for the resource's URI so we don't collide with other
    # tests.
    uri = f'tests/{uuid1()}.xml'

    # Check that it doesn't exist.
    assert_document_not_found(client, uri)

    # Create the XML resource.
    with open('tests/test_data/test_data.xml', 'r+b') as file_handle:
        response = client.create_xml(uri, file_handle)
        assert response.ok
        assert response.status_code == 201  # Created

    # Check that it exists.
    assert_document_found(client, uri)

    # Clean up the created resource afterwards.
    response = client.delete_document(uri)
    assert response.ok

    # Check that it doesn't exist anymore.
    assert_document_not_found(client, uri)


def test_json():
    """Test creating, getting, and deleting of a JSON document"""
    enable_http_logging()

    client = make_client()

    # Generate a UUID for the resource's URI so we don't collide with other
    # tests.
    uri = f'tests/{uuid1()}.json'

    # Check that it doesn't exist.
    assert_document_not_found(client, uri)

    # Create a JSON resource.
    with open('tests/test_data/test_data.json', 'r+b') as file_handle:
        response = client.create_json(uri, file_handle)
        assert response.ok
        assert response.status_code == 201  # Created

    # Check that it exists.
    assert_document_found(client, uri)

    # Clean up the created resource afterwards.
    response = client.delete_document(uri)
    assert response.ok

    # Check that it doesn't exist anymore.
    assert_document_not_found(client, uri)


def assert_graph_not_found(client, graph_uri):
    """Asserts that there is no graph with the given URI, reached by the given
    client.
    """
    response = client.get_graph(graph_uri)
    assert response.status_code == 404  # Not Found
    assert not response.ok
    
    
def assert_graph_found(client, graph_uri):
    """Asserts that there is a graph with the given URI, reached by the given
    client.
    """
    response = client.get_graph(graph_uri)
    assert response.status_code == 200  # OK
    assert response.ok


def test_create_triples():
    """Test creating triples"""
    enable_http_logging()

    client = make_client()

    # Generate a UUID for the graph's URI so we don't collide with other tests.
    graph_uri = f'{uuid1()}_test_graph'

    # Check that the graph doesn't exist beforehand.
    assert_graph_not_found(client, graph_uri)

    # Upload some triples
    with open('tests/test_data/test_data.ttl', 'r+b') as file_handle:
        response = client.create_triples_ttl(file_handle, graph_uri=graph_uri)
        assert response.ok

    # Check that the graph exists now.
    response = client.get_graph(graph_uri)
    assert response.ok

    # Check something trivial that should be in the triples.
    assert "costPerItem" in response.text

    # Clean up the graph (and triples) afterwards.
    response = client.delete_graph(graph_uri)
    assert response.ok

    # Check that the graph doesn't exist anymore.
    assert_graph_not_found(client, graph_uri)

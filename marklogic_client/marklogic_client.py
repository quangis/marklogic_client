"""This module has a MarkLogic client that can create, retrieve, and delete
various types of resources on a MarkLogic server.
"""

import requests
from requests.auth import HTTPDigestAuth

class MarkLogicClient:
    """This class can create, retrieve, and delete resources on a MarkLogic
    server.
    """

    def __init__(self, url, username, password, api_version='LATEST'):
        self.session = start_session(username, password)
        self.url = url
        self.api_version = api_version

    def create_document(self, uri, data, content_type):
        """Create a document with the given data and content."""
        return self.session.put(
            f'{self.url}/{self.api_version}/documents',
            data=data,
            params={'uri': uri},
            headers={'Content-type': content_type}
        )

    def create_xml(self, uri, data):
        """Create an XML document with the given data."""
        return self.create_document(uri, data, 'application/xml')

    def create_json(self, uri, data):
        """Create JSON document with the given data."""
        return self.create_document(uri, data, 'application/json')

    def get_document(self, uri):
        """Retrieve the document at the specified URI."""
        return self.session.get(
            f'{self.url}/{self.api_version}/documents',
            params={'uri': uri}
        )

    def delete_document(self, uri):
        """Delete the resource at the specified URI."""
        return self.session.delete(
            f'{self.url}/{self.api_version}/documents',
            params={'uri': uri}
        )

    def create_triples(self, data, content_type, graph_uri=None):
        """Add (merge) the given triples in the given data to the default
        graph, or when `graph` is given, add it to that graph.
        """
        if graph_uri is not None:
            params = {'graph': graph_uri}
        else:
            params = {'default': ''}
        return self.session.post(
            f'{self.url}/{self.api_version}/graphs',
            data=data,
            params=params,
            headers={'Content-type': content_type}
        )

    def create_triples_rdf_xml(self, data, graph_uri=None):
        """Add (merge) the given RDF/XML triples in the given data to the
        default graph, or when `graph` is given, add it to the graph with that
        name.
        """
        return self.create_triples(data, 'application/rdf+xml',
                                   graph_uri=graph_uri)

    def create_triples_ttl(self, data, graph_uri=None):
        """Add (merge) the given Turtle triples in the given data to the
        default graph, or when `graph` is given, add it to the graph with that
        name.
        """
        return self.create_triples(data, 'text/turtle', graph_uri=graph_uri)

    def get_graph(self, graph_uri):
        """Retrieve the graph at the specified URI."""
        return self.session.get(
            f'{self.url}/{self.api_version}/graphs',
            params={
                'graph': graph_uri
            }
        )

    def delete_graph(self, graph_uri):
        """Delete the graph at the specified URI."""
        return self.session.delete(
            f'{self.url}/{self.api_version}/graphs',
            params={
                'graph': graph_uri
            }
        )


def start_session(username, password):
    """Start a new session using digest authentication and the given credentials."""
    session = requests.Session()
    session.auth = HTTPDigestAuth(username, password)
    return session

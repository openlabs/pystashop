# -*- coding: utf-8 -*-
"""
    api


    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import os
from collections import namedtuple
import pkg_resources

from pystashop.api import PrestaShopWebservice, singular, ResourceProxy

Response = namedtuple('Response', 'status_code, content')


class FakeSession(object):
    """
    A requests.Session like class which just checks the filesystem folder
    for a possible xml to return
    """
    def __init__(self, version):
        self.version = version

    @property
    def folder(self):
        """
        Return the folder where the xml files are stored
        """
        root_xml_folder = pkg_resources.resource_filename('mockstashop', 'xml')

        # XXX: May be handle minor versions if there are API changes inside
        # minor releases ?
        return os.path.join(root_xml_folder, self.version)

    @staticmethod
    def get_path(url):
        """
        Return just the path of the url

        >>> FakeSession.get_path('/api/customers')
        'customers.xml'
        >>> FakeSession.get_path('/api/customers/1')
        'customers/1.xml'
        >>> FakeSession.get_path('/api/orders')
        'orders.xml'

        :param url: URL of the file
        """
        # Different resources like customers, orders as each of them have files
        # names like 1.xml, 2.xml for individual records.
        # If the last part of URL is an integer, return last two parts of URL
        first, second_last, last = url.rsplit('/', 2)

        if last.isdigit():
            return os.path.join(second_last, last + '.xml')
        else:
            # If the last part is not an integer, return last part itself
            return last + '.xml'

    def build_response_for(self, path):
        """
        Build a mock http response with code and content

        :param path: Path to file inside self.folder
        """
        filename = os.path.join(self.folder, path)
        if os.path.exists(filename):
            return Response(
                status_code=200,
                content=open(filename).read()
            )
        else:
            return Response(
                status_code=404,
                content=open(os.path.join(self.folder, 'error.xml')).read()
            )

    def get(self, url, params=None):
        """
        A GET request is made to the URL

        :param url: URL of the file
        :param params: Parameters used for filtering of records.
                       This is not implemented yet.
        """
        # TODO: handle params
        path = self.get_path(url)
        return self.build_response_for(path)


class MockstaShopWebservice(PrestaShopWebservice):
    """
    A mock service client for prestashop


    `Read More <http://doc.prestashop.com/display/PS14/\
                Chapter+1+-+Creating+Access+to+Back+Office>`_
    """

    def __init__(self, url, key, debug=False):
        """
        :param url: The store's root path (ex: http://store.com/ )
        :param key: The authentication key (ex: ZR92FNY5UFRERNI3O9Z5QDHWKTP3Y)
        :param debug: A Boolean indicating whether the Web service must use
                      its debug mode
        """
        self.url = url
        if self.url.endswith('/'):
            self.url = self.url[:-1]
        self.key = key
        self.debug = debug
        self.version = '1.5'

    @property
    def session(self):
        """Generate a fake requests session
        """
        if not hasattr(self, '_session'):
            self._session = FakeSession(self.version)
            self._session.auth = (self.key, 'ignore')
        return self._session

    def __getattr__(self, name):
        """
        Return a Resource proxy object for the attribute

        :param name: Name of the resource
        """
        return type(
            'MockstaShopWebservice.' + name,
            (MockResourceProxy,),
            {
                '__resource__': name,
                'session': self.session,
                '__version__': self.version,
                'url': '{0}/api/{1}'.format(self.url, name)
            }
        )


class MockResourceProxy(ResourceProxy):
    """
    Class to represent any resource on prestashop
    """

    @classmethod
    @singular
    def create(cls, xml):
        """
        Creates a record on the server

        :param xml: XML for which record needs to be created
        """
        raise Exception('Not Implemented Yet')

    @classmethod
    def update(cls, id, xml):
        """
        Updates a single record on the server

        :param id: ID of the record to be updated
        :param xml: Details to be updated in XML
        """
        raise Exception('Not Implemented Yet')

    @classmethod
    def delete(cls, id):
        """
        Deletes a single record from the server

        :param id: ID of record to be deleted

        :return: True if deletion was successful
        """
        raise Exception('Not Implemented Yet')

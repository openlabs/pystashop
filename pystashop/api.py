# -*- coding: utf-8 -*-
"""
    api


    :copyright: © 2013 by Openlabs Technologies & Consulting (P) Limited
    :license: BSD, see LICENSE for more details.
"""
import functools

import requests
from lxml import objectify, etree


class PrestaShopWebserviceException(Exception):
    """
    Abstract Exception class for all exceptions
    """
    pass


class PrestaShopWebservice(object):
    """
    Web service client for prestashop

    Use of this API requires an authentication key. If you do not have one,
    you can generate one from your Back Office and click on the
    "Tools / Web Service" tab.

    `Read More <http://doc.prestashop.com/display/PS14/Chapter+1+-+Creating+Access+to+Back+Office>`_
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

    @property
    def session(self):
        if not hasattr(self, '_session'):
            self._session = requests.Session()
            self._session.auth = (self.key, 'ignore')
        return self._session

    def __getattr__(self, name):
        """
        Return a Resource proxy object for the attribute
        """
        return type(
            'PrestaShopWebservice.' + name,
            (ResourceProxy,),
            {
                '__resource__': name,
                'session': self.session,
                'url': '{0}/api/{1}'.format(self.url, name)
            }
        )


def singular(function):
    @functools.wraps(function)
    def wrapper(cls, *args, **kwargs):
        rv = function(cls, *args, **kwargs)
        return rv.getchildren()[0]
    return wrapper


class ResourceProxy(object):
    """
    Class to represent any resource on prestashop
    """

    @classmethod
    def check_status(cls, response):
        """
        Check the response status code and if it is not one of the
        HTTP OK codes, raise an exception with the content of the response

        :param response: response object from requests
        """
        if response.status_code not in (200, 201):
            raise PrestaShopWebserviceException(response.content)

    @classmethod
    def wrap_in_prestashop_tag(cls, child):
        """
        Wrap the given Element child into a prestashop root
        tag and deannotate elements.

        :param child: lxml Element
        """
        root = objectify.Element('prestashop')
        root.insert(0, child)
        objectify.deannotate(root)
        return root

    @classmethod
    @singular
    def create(cls, xml):
        """
        Creates a record on the server
        """
        root = cls.wrap_in_prestashop_tag(xml)
        response = cls.session.post(
            cls.url, data={'xml': etree.tostring(root)}
        )
        cls.check_status(response)

        return objectify.fromstring(response.content)

    @classmethod
    @singular
    def get_schema(cls):
        """
        Returns a blank xml
        """
        response = cls.session.get(cls.url + '?schema=blank')
        cls.check_status(response)

        return objectify.fromstring(response.content)

    @staticmethod
    def make_params(display=None, filters=None, sort=None, limit=None, offset=None):
        """
        Builds the URL paramters as a dictionary

        :param display: A list of field names
                        eg: ['firstname', 'lastname']
        :param filters: A dictionary of field name and values
                        eg: {'firstname': 'sharoon'}
        :param sort: a list of tuple of field and value
                     eg: [('firstname', 'ASC'), ('lastname', 'DESC')]
        :param limit: The number of records to be returned
        :param offset: The number of records to skip
        """
        params = {}

        if display:
            params['display'] = '[' + ','.join(display) + ']'

        if filters:
            for key, value in filters.iteritems():
                params['filter[%s]' % key] = '[%s]' % value

        if sort:
            params['sort'] = '[' + ','.join([
                '{0}_{1}'.format(field, order) for field, order in sort
            ]) + ']'

        if limit and not offset:
            params['limit'] = limit
        elif limit and offset:
            params['limit'] = '%d,%d' % (offset - 1, limit)

        return params

    @classmethod
    def get_list(cls, as_ids=False, display=None,
                 filters=None, sort=None, limit=None, offset=None):
        """
        Gets a list of records by sending GET on the Collection
        URI of the resource.

        :param as_ids: If True a list of ids are returned, or the
                       XML object is returned
        :param display: A list of fields that needs to be returned.
                        By default only the ID is fetched
        """
        if display is None:
            display = []

        if as_ids and 'id' not in display:
            display.append('id')

        params = cls.make_params(display, filters, sort, limit, offset)

        response = cls.session.get(cls.url, params=params)
        cls.check_status(response)
        rv = objectify.fromstring(response.content)


        if as_ids:
            return map(
                lambda r: int(r.id),
                getattr(rv, cls.__resource__).iterchildren()
            )

        return getattr(rv, cls.__resource__).getchildren()

    @classmethod
    @singular
    def get(cls, id):
        """
        Reads a single record from the server

        :param id: Id of the record to read
        """
        response = cls.session.get('%s/%d' % (cls.url, id))
        cls.check_status(response)
        return objectify.fromstring(response.content)

    @classmethod
    def update(cls, id, xml):
        """
        Updates a single record on the server
        """
        root = cls.wrap_in_prestashop_tag(xml)

        response = cls.session.put(
            '%s/%d' % (cls.url, id),
            data=etree.tostring(root)
        )
        cls.check_status(response)

        return objectify.fromstring(response.content)

    @classmethod
    def delete(cls, id):
        """
        Deletes a single record from the server

        :return: True if deletion was successful
        """
        response = cls.session.delete('%s/%d' % (cls.url, id))
        cls.check_status(response)
        return response.status_code == requests.codes.ok

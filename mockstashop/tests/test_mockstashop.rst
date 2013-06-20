===================
Testing mockstashop
===================

Connecting to your store::

    >>> import os
    >>> from mockstashop.api import MockstaShopWebservice, FakeSession
    >>> from pystashop.api import PrestaShopWebserviceException
    >>> from datetime import datetime, timedelta
    >>> from lxml import objectify
    >>> client = MockstaShopWebservice('Some URL', 'Some Key')

Getting a list of customers::

    >>> customers = client.customers.get_list(as_ids=True)
    >>> type(customers)
    <type 'list'>
    >>> customers_count = len(customers)
    >>> customers_count
    5

Getting a single customer record::

    >>> customer = client.customers.get(1)
    >>> customer.firstname
    'John'
    >>> customer.lastname
    'DOE'
    >>> customer.email
    'pub@prestashop.com'

Getting a single order record::

    >>> order = client.orders.get(1)
    >>> order.reference
    'XKBKNABJK'
    >>> order.id_customer
    1

Test the validity of xml files::

    >>> folder_path = FakeSession('1.5').folder
    >>> for root, dirs, files in os.walk(folder_path):
    ...     for file in files:
    ...         if file.endswith('.xml'):
    ...             response = objectify.fromstring(
    ...                 open(os.path.join(root, file)).read() \
    ...             )

Test the get_path method::

    >>> FakeSession.get_path('/api/customers')
    'customers.xml'
    >>> FakeSession.get_path('/api/customers/1')
    'customers/1.xml'
    >>> FakeSession.get_path('/api/orders')
    'orders.xml'

Test the error file::

    >>> try:
    ...     client.shops.get(10)
    ... except PrestaShopWebserviceException, exc:
    ...     error = objectify.fromstring(exc.message)
    >>> error.getchildren()[0].error.message
    '\n                    Error XML. File not found.\n                \n            '

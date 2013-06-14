Python API for Prestashop
=========================

The Python API for prestashop

Running the test against an existing server:
--------------------------------------------

This file is also a test written in the doctest format. To run the example
in this file against your installation of prestashop, replace the api key
in the below example and run this file from the doctest module

.. code:: sh

    $ python -m doctest -v README.rst


Example Usage:
--------------

Connecting to your store::

    >>> from pystashop import PrestaShopWebservice
    >>> from datetime import datetime, timedelta
    >>> client = PrestaShopWebservice(
    ...     'http://prestashop.openlabs.co.in', 
    ...     'X76XVCPE71843TIY5CPJVV3NX56Z4MVD')

Getting a list of customers::

    >>> customers = client.customers.get_list(as_ids=True)
    >>> type(customers)
    <type 'list'>
    >>> customers_count = len(customers)

Creating customers::

    >>> new_customer = client.customers.get_schema()
    >>> new_customer.firstname = 'Sharoon'
    >>> new_customer.lastname = 'Thomas'
    >>> new_customer.email = 'st@openlabs.co.in'
    >>> customer = client.customers.create(new_customer)
    >>> customer.firstname
    'Sharoon'
    >>> customer.lastname
    'Thomas'
    >>> new_customer2 = client.customers.get_schema()
    >>> new_customer2.firstname = 'Test'
    >>> new_customer2.lastname = 'Customer'
    >>> new_customer2.email = 'test@openlabs.co.in'
    >>> customer2 = client.customers.create(new_customer2)
    >>> customers_list = client.customers.get_list(as_ids=True)
    >>> len(customers_list) == customers_count + 2
    True
    >>> customer.id in customers_list
    True

Getting a single customer record::

    >>> customer = client.customers.get(customer.id)
    >>> customer.firstname
    'Sharoon'
    >>> customer.lastname
    'Thomas'

Editing the customer details::

    >>> customer.email = 'info@openlabs.co.in'
    >>> result = client.customers.update(customer.id, customer)
    >>> updated_data = client.customers.get(customer.id)
    >>> updated_data.email
    'info@openlabs.co.in'


Choosing fields to display::

    >>> customers = client.customers.get_list(
    ...     display=['id', 'firstname', 'lastname']
    ... )
    >>> isinstance(customers[0].firstname.pyval, basestring)
    True
    >>> isinstance(customers[0].lastname.pyval, basestring)
    True
    >>> isinstance(customers[0].id.pyval, int)
    True

Filtering Records to Display::

    >>> customers = client.customers.get_list(
    ...     filters={'firstname': 'Sharoon'},
    ...     display=['firstname']
    ... )
    >>> customers[0].firstname.pyval
    'Sharoon'

Filtering Records on basis of date::

    >>> customers = client.customers.get_list(
    ...     filters={
    ...         'date_add': '{0},{1}'.format(
    ...             '2012-01-01 00:00:00',
    ...             datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    ...         ),
    ...         'firstname': 'Sharoon',
    ...     },
    ...     display=['firstname'], date=True,
    ... )
    >>> customers[0].firstname.pyval
    'Sharoon'
    >>> time_diff = timedelta(hours=5)
    >>> time_now = datetime.utcnow()
    >>> customers = client.customers.get_list(
    ...     filters={
    ...         'date_add': '{0},{1}'.format(
    ...             time_now.strftime('%Y-%m-%d %H:%M:%S'),
    ...             (time_now + time_diff).strftime(
    ...                 '%Y-%m-%d %H:%M:%S')
    ...         ),
    ...         'firstname': 'Sharoon',
    ...     },
    ...     display=['firstname'], date=True,
    ... )
    >>> len(customers)
    0

Sorting Records to be displayed::

    >>> customers = client.customers.get_list(
    ...     display=['firstname'],
    ...     sort=[('firstname', 'DESC')]
    ... )
    >>> customers[0].firstname.pyval
    'Test'
    >>> customers = client.customers.get_list(
    ...     display=['lastname'],
    ...     sort=[('lastname', 'DESC')]
    ... )
    >>> customers[0].lastname.pyval
    'Thomas'

Limiting and offsetting records to be displayed::

    >>> customer_list1 = client.customers.get_list(
    ...     as_ids=True, limit=1
    ... )
    >>> len(customer_list1)
    1
    >>> customer_list2 = client.customers.get_list(
    ...     as_ids=True, offset=2, limit=1
    ... )
    >>> len(customer_list2)
    1
    >>> customer_list1 == customer_list2
    False

Deleting a customer::

    >>> client.customers.delete(customer.id)
    True
    >>> customers_list = client.customers.get_list(as_ids=True)
    >>> len(customers_list) == customers_count + 1
    True
    >>> customer.id in customers_list
    False

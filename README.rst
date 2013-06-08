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
    >>> client = PrestaShopWebservice(
    ...     'http://prestashop.openlabs.co.in', 
    ...     'X76XVCPE71843TIY5CPJVV3NX56Z4MVD')

Getting a list of customers::

    >>> customers = client.customers.get_list(as_ids=True)
    >>> type(customers)
    <type 'list'>
    >>> customers_count = len(customers)

Creating a customer::

    >>> new_customer = client.customers.get_schema()
    >>> new_customer.firstname = 'Sharoon'
    >>> new_customer.lastname = 'Thomas'
    >>> new_customer.email = 'st@openlabs.co.in'
    >>> customer = client.customers.create(new_customer)
    >>> customer.firstname
    'Sharoon'
    >>> customer.lastname
    'Thomas'
    >>> customers_list = client.customers.get_list()
    >>> len(customers_list) == customers_count + 1
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

    >>> customers = client.customers.get_list(display=['firstname', 'lastname'])
    >>> isinstance(customers[0].firstname.pyval, basestring)
    True
    >>> isinstance(customers[0].lastname.pyval, basestring)
    True
    >>> isinstance(customers[0].id.pyval, int)
    True

Filtering Records to Display::

    >>> customers = client.customers.get_list(filters={'firstname': 'Sharoon'})
    >>> customers[0].firstname
    Sharoon

Deleting a customer::

    >>> client.customers.delete(customer.id)
    True
    >>> customers_list = client.customers.get_list()
    >>> len(customers_list) == customers_count
    True
    >>> customer.id in customers_list
    False


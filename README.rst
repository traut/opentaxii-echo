opentaxii-echo
==============

Simple Echo implementation of OpenTAXII Persistence API.
--------------------------------------------------------

Echo Persistence API is fully stateless implementation of OpenTAXII Persistence API. The state of a TAXII server is defined by state parameters in a GET query.

For example, Discovery request sent to::

    http://localhost:9000/discovery/?services=poll,inbox,discovery&discovery_advertised=inbox,poll

will return Discovery response with 2 services advertised: Poll and Inbox.

Supported state parameters:

.. list-table::
    :header-rows: 1

    * - Parameter
      - Value
      - Defaults
      - Example
    * - ``services``
      - comma separated list of active services. Supported values are ``poll``, ``inbox``, ``collection_management``, ``discovery``
      - ``discovery``, ``collection_management``, ``poll``, ``inbox``
      - ``?services=collection_management,discovery``
    * - ``discovery_advertised``
      - comma separated list of advertised services
      - ``discovery``, ``collection_management``, ``poll``, ``inbox``
      - ``?discovery_advertised=poll,inbox,discovery``
    * - ``*_address``
      - service address; ``*`` replaced with a service
      - ``/discovery/``, ``/collection_management/``, ``/poll/``, ``/inbox/``
      - ``?inbox_address=/service/inbox``
    * - ``*_description``
      - service description; ``*`` replaced with a service
      - 
      - ``?poll_description=TestDescription``
    * - ``collections``
      - comma separated list of the collection names
      - ``alien-encounters``, ``traces-of-evil-ninjas``
      - ``?collections=collection-a,collection-b``
    * - ``*_supported_content``
      - comma separated list of supported content bindings for a collection; ``*`` replaced with a collection name
      - 
      - ``?collection-a_supported_content=foo,bar``
    * - ``*_count``
      - blocks count for a collection; ``*`` replaced with a collection name
      - 0
      - ``?collection-a_count=100&bbb_count=1``
    * - ``use_cosive``
      - Use `Cosive <http://cosive.com>`_ free STIX API to fill content blocks with STIX packages.
      - ``true``
      - ``?use_cosive=no``
    * - ``cosive_objects``
      - Specify what objets should Cosive API put in STIX. See https://generator.cosive.com/ for details.
      -
      - ``?cosive_objects=url,domain``
    * - ``cosive_count``
      - Specify how many objects put into STIX package. See https://generator.cosive.com/ for details.
      -
      - ``?cosive_count=1``
    * - ``content_blocks``
      - how many content block to return in Poll response.
      - 2
      - ``?conent_blocks=10``
    * - ``binding``
      - content binding of the content blocks to return
      - ``urn:stix.mitre.org:xml:1.1.1``
      - ``?binding=urn:stix.mitre.org:xml:1.1.1``

Using `Cabby <https://pypi.python.org/pypi/cabby>`_  TAXII client, the requests can look like:

* Discovery request:

.. code-block:: bash

    $ taxii-discovery --path "http://localhost:9000/discovery/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&inbox_address=/some/inbox&poll_description=dummy-description"

* Collection Management request:

.. code-block:: bash

    $ taxii-collections --path "http://localhost:9000/collections/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&collection_management_address=/collections/&inbox_address=/some/inbox&poll_description=WHAT?&collections=aaa,bbb,ccc&aaa_supported_content=foo,bar&aaa_count=123&bbb_count=999"

* Poll request:

.. code-block:: bash

    $ taxii-poll --path "http://localhost:9000/poll/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&collection_management_address=/collections/&inbox_address=/some/inbox&poll_description=WHAT?&collections=aaa,bbb,ccc&aaa_supported_content=foo,bar&aaa_count=123&bbb_count=999&return_blocks=100" -c bbb


Running a server
----------------
To run a server, specify a configuration file ``opentaxii-config.yml`` as ``OPENTAXII_CONFIG`` variable:

.. code-block:: bash

    OPENTAXII_CONFIG=./opentaxii-config.yml opentaxii-run-dev

Body of ``opentaxii-config.yml`` can be:

.. code-block:: yaml

    ---
    persistence_api:
      class: opentaxii_echo.persistence.EchoPersistenceAPI
      parameters:

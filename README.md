# opentaxii-echo

Simple Echo implementation of OpenTAXII Persistence API

Control parameters are passed in GET query:

|        parameter         |                value                             |                value example                  |
|--------------------------|--------------------------------------------------|-----------------------------------------------|
| ``services``             | comma separated list of active services          | ``services=collection_management,discovery``  |
| ``discovery_advertised`` | comma separated list of adcertised services      | ``discovery_advertised=poll,inbox,discovery`` |
| ``*_address``            | service address, ``*`` replaced with service     | ``inbox_address=/service/inbox``              |
| ``*_description``        | service description, ``*`` replaced with service | ``poll_description=TestDescription``          |
| ``collections``          | comma separated list of collection names         | ``collections=collection-a,collection-b``     |
| ``*_supported_content``  | comma separated list of supported content bindings for a collection  | ``collection-a_supported_content=foo,bar`` |
| ``*_count``              | block counts for a collection,  | ``collection-a_count=100&bbb_count=1`` |


```
#!/bin/bash

taxii-collections --path "http://localhost:9000/collections/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&collection_management_address=/collections/&inbox_address=/some/inbox&poll_description=WHAT?&collections=aaa,bbb,ccc&aaa_supported_content=foo,bar&aaa_count=123&bbb_count=999"

taxii-poll --path "http://localhost:9000/poll/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&collection_management_address=/collections/&inbox_address=/some/inbox&poll_description=WHAT?&collections=aaa,bbb,ccc&aaa_supported_content=foo,bar&aaa_count=123&bbb_count=999&blocks_count=100" -c bbb
```

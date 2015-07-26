#!/bin/bash

taxii-poll --path "http://localhost:9000/poll/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&collection_management_address=/collections/&inbox_address=/some/inbox&poll_description=WHAT?&collections=aaa,bbb,ccc&aaa_supported_content=foo,bar&aaa_count=123&bbb_count=999&return_blocks=100" -c bbb

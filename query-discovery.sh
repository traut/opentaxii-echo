#!/bin/bash

taxii-discovery --path "http://localhost:9000/discovery/?services=poll,inbox,collection_management,discovery&discovery_advertised=inbox,poll&inbox_address=/some/inbox&poll_description=dummy-description"

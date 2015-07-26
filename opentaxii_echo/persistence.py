import structlog
import uuid
import inspect
import pytz
from datetime import datetime

from flask import request, abort
from libtaxii.constants import VID_TAXII_HTTP_10

from opentaxii.server import TAXIIServer
from opentaxii.taxii.services.abstract import TAXIIService
from opentaxii.persistence.api import OpenTAXIIPersistenceAPI

from opentaxii.taxii.entities import (
    ContentBindingEntity, CollectionEntity, ContentBlockEntity,
    ServiceEntity, ResultSetEntity
)

log = structlog.getLogger(__name__)


class EchoPersistenceAPI(OpenTAXIIPersistenceAPI):

    def __init__(self):
        pass

    @property
    def config(self):
        if not request.args:
            log.error("request.no_arguments")
            abort(405)
        return request.args

    def get_services(self, collection_id=None):

        service_types = map(lambda s: s.lower(),
                            self.config.get('services', '').split(','))

        services = []
        for service_type in service_types:
            if service_type not in TAXIIServer.TYPE_TO_SERVICE:
                log.error("service.type.unknown", service_type=service_type)
                abort(405)

            service_class = TAXIIServer.TYPE_TO_SERVICE[service_type]

            args = []
            args.extend(inspect.getargspec(TAXIIService.__init__).args)
            args.extend(inspect.getargspec(service_class.__init__).args)
            args.remove('self')
            args.remove('path')

            properties = {
                'address': '/{}/'.format(service_type),
                'protocol_bindings': [VID_TAXII_HTTP_10]
            }

            for arg in args:
                value = self.config.get(
                    '{}_{}'.format(service_type, arg))

                if value:
                    properties[arg] = value

            service = ServiceEntity(
                id=service_type,
                type=service_type,
                properties=properties
            )
            if service_type == 'discovery':

                service.properties['advertised_services'] = \
                    self.config.get('discovery_advertised', [])

            services.append(service)

        if collection_id:
            pass
        else:
            pass

        return services

    def create_content_block(self, block, service_id, collection_ids=None):
        pass

    def create_result_set(self, result_set_entity):
        result_set_entity.id = str(uuid.uuid4())
        return result_set_entity

    def get_result_set(self, result_set_id):

        content_binding = self.config.get('binding', 'dummy-binding')

        class DummyCollection(object):
            def __ne__(self, other):
                return False

        return ResultSetEntity(
            result_set_id,
            DummyCollection(),
            content_bindings=[content_binding],
            timeframe=None
        )

    def get_collections(self, service_id):

        collection_names = self.config.get('collections', '').split(',')

        collections = []
        for name in collection_names:

            content_type_key = '{}_supported_content'.format(name)
            content_types = (self.config
                                 .get(content_type_key, '')
                                 .split(','))

            collection = CollectionEntity(
                id=name,
                name=name,
                available=True,
                supported_content=content_types,
                accept_all_content=True,
            )
            collections.append(collection)

        return collections

    def get_collection(self, collection_name, service_id):

        content_type_key = '{}_supported_content'.format(collection_name)
        content_types = (self.config
                             .get(content_type_key, '')
                             .split(','))

        return CollectionEntity(
            id=collection_name,
            name=collection_name,
            available=True,
            supported_content=content_types,
            accept_all_content=True,
        )

    def create_inbox_message(self, inbox_message_entity):
        pass

    def get_content_blocks_count(self, collection_id, start_time=None,
                                 end_time=None, bindings=[]):
        return int(self.config.get('{}_count'.format(collection_id), 0))

    def get_content_blocks(self, collection_id, start_time=None, end_time=None,
                           bindings=[], offset=0, limit=None):

        return_blocks = int(self.config.get('return_blocks', 0))
        blocks = []
        for i in range(0, return_blocks):
            content_binding = self.config.get('binding', 'dummy-binding')

            blocks.append(ContentBlockEntity(
                content="CONTENT-BLOCK-{}".format(i),
                timestamp_label=datetime.utcnow().replace(tzinfo=pytz.UTC),
                content_binding=ContentBindingEntity(content_binding)
            ))

        return blocks

    def get_domain(self, service_id):
        return self.config.get('domain')

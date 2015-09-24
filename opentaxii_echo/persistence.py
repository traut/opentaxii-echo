from datetime import datetime
import inspect

import structlog
import uuid
import pytz
import requests
from werkzeug.datastructures import MultiDict
from flask import request, abort, current_app
from libtaxii.constants import VID_TAXII_HTTP_10, CB_STIX_XML_111

from opentaxii.server import TAXIIServer
from opentaxii.taxii.services.abstract import TAXIIService
from opentaxii.persistence.api import OpenTAXIIPersistenceAPI

from opentaxii.taxii.entities import (
    ContentBindingEntity, CollectionEntity, ContentBlockEntity,
    ServiceEntity, ResultSetEntity
)

log = structlog.getLogger(__name__)


def normalize(config, key):
    if (config.get(key) and isinstance(config[key], basestring)):
        config[key] = map(lambda s: s.lower(), config[key].split(','))


class EchoPersistenceAPI(OpenTAXIIPersistenceAPI):

    def __init__(self):
        pass

    @property
    def config(self):
        config = dict(current_app.taxii.config)

        for arg in request.args:
            config[arg] = request.args.get(arg)

        if (config.get('services')
                and isinstance(config['services'], basestring)):
            config['services'] = map(lambda s: s.lower(),
                                     config['services'].split(','))
        normalize(config, 'services')
        normalize(config, 'collection_names')
        normalize(config, 'discovery_advertised')

        return config

    def get_services(self, collection_id=None):

        services = []
        for service_type in self.config.get('services', []):
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
                value = self.config.get('{}_{}'.format(service_type, arg))
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

        content_binding = self.config.get('binding', CB_STIX_XML_111)

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

        collections = []
        for name in self.config.get('collection_names', []):

            content_type_key = '{}_supported_content'.format(name)
            content_types = map(lambda x: x.lower(),
                                self.config
                                    .get(content_type_key, '')
                                    .split(','))

            collection = CollectionEntity(
                id=name,
                name=name,
                available=True,
                supported_content=content_types,
                accept_all_content=True,
                volume=0,
            )
            collections.append(collection)

        return collections

    def get_collection(self, collection_name, service_id):

        if collection_name not in self.config.get('collection_names', []):
            return None

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
            volume=0,
        )

    def create_inbox_message(self, inbox_message_entity):
        pass

    def get_content_blocks_count(self, collection_id, start_time=None,
                                 end_time=None, bindings=[]):

        return int(self.config.get('{}_count'.format(collection_id), 0))

    def _get_cosive_content(self, version):

        url = 'https://api.cosive.com/sdg/v1/stix'

        objects = self.config.get('cosive_objects')
        count = int(self.config.get('cosive_count', 1))

        r = requests.get(url, params={
            version: version,
            objects: objects,
            count: count
        })

        if r.status_code != 200:
            log.error("cosive.response.status_code",
                      status_code=r.status_code, response=r.text)
            return None

        return r.text


    def get_content_blocks(self, collection_id, start_time=None, end_time=None,
                           bindings=[], offset=0, limit=None):

        content_blocks = int(self.config.get('content_blocks', 0))
        content_binding = self.config.get('binding', CB_STIX_XML_111)

        use_cosive = str(self.config.get('use_cosive', "true"))
        use_cosive = use_cosive.lower() == "true"

        blocks = []

        for i in range(0, content_blocks):

            if use_cosive:
                if content_binding == 'urn:stix.mitre.org:xml:1.1.1':
                    version = '1.1.1'
                elif content_binding == 'urn:stix.mitre.org:xml:1.2':
                    version = '1.2'
                else:
                    version = None
                    log.error("Cosive only supports STIX 1.1.1 and 1.2")

            content = "CONTENT-BLOCK-{}".format(i)

            if use_cosive and version:
                content = self._get_cosive_content(version) or content

            blocks.append(ContentBlockEntity(
                content=content,
                timestamp_label=datetime.utcnow().replace(tzinfo=pytz.UTC),
                content_binding=ContentBindingEntity(content_binding)
            ))

        return blocks

    def get_domain(self, service_id):
        return self.config.get('domain')

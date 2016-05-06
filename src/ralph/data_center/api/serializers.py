# -*- coding: utf-8 -*-
from rest_framework import serializers

from ralph.api import RalphAPISerializer
from ralph.assets.api.serializers import AssetSerializer, BaseObjectSerializer
from ralph.assets.models.components import Ethernet
from ralph.data_center.models import (
    Accessory,
    Cluster,
    ClusterType,
    Database,
    DataCenter,
    DataCenterAsset,
    Rack,
    RackAccessory,
    ServerRoom,
    VIP
)


class ClusterTypeSerializer(RalphAPISerializer):
    class Meta:
        model = ClusterType
        depth = 1


class ClusterSimpleSerializer(BaseObjectSerializer):
    class Meta(BaseObjectSerializer.Meta):
        model = Cluster
        exclude = ('content_type',)
        depth = 1


class ClusterSerializer(ClusterSimpleSerializer):
    base_objects = serializers.HyperlinkedRelatedField(
        many=True, view_name='baseobject-detail', read_only=True
    )

    class Meta(ClusterSimpleSerializer.Meta):
        pass


class DataCenterSerializer(RalphAPISerializer):
    class Meta:
        model = DataCenter
        depth = 1


class ServerRoomSerializer(RalphAPISerializer):
    class Meta:
        model = ServerRoom
        depth = 1


class AccessorySerializer(RalphAPISerializer):
    class Meta:
        model = Accessory


class RackAccessorySerializer(RalphAPISerializer):
    name = serializers.ReadOnlyField(source='accessory.name')

    class Meta:
        model = RackAccessory


class SimpleRackSerializer(RalphAPISerializer):
    class Meta:
        model = Rack
        depth = 2
        exclude = ('accessories',)


class EthernetSerializer(RalphAPISerializer):
    class Meta:
        model = Ethernet
        depth = 1


class ComponentSerializerMixin(serializers.Serializer):
    ethernets = EthernetSerializer()
    # disk_shares = ..
    # ipaddresses = SimpleIPAddressesSerializer()
    # mac_addresses = SimpleRackSerializer()
    service = serializers.SerializerMethodField('get_service_env')

    def get_service_env(self, obj):
        return ''


class RackSerializer(RalphAPISerializer):
    accessories = RackAccessorySerializer(
        read_only=True, many=True, source='rackaccessory_set'
    )

    class Meta(SimpleRackSerializer.Meta):
        model = Rack
        depth = 2
        exclude = ()


class DataCenterAssetSimpleSerializer(RalphAPISerializer):
    class Meta:
        model = DataCenterAsset
        fields = ['hostname', 'url']
        _skip_tags_field = True


class DataCenterAssetSerializer(ComponentSerializerMixin, AssetSerializer):
    rack = SimpleRackSerializer()

    class Meta(AssetSerializer.Meta):
        model = DataCenterAsset
        depth = 1


class DatabaseSerializer(BaseObjectSerializer):
    class Meta(BaseObjectSerializer.Meta):
        model = Database
        depth = 1


class VIPSerializer(BaseObjectSerializer):
    class Meta(BaseObjectSerializer.Meta):
        model = VIP
        depth = 1

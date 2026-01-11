from rest_framework import serializers

class EnqueueSerializer(serializers.Serializer) :
    type = serializers.CharField()
    payload = serializers.DictField()
    retries = serializers.IntegerField(min_value = 0, max_value = 5)
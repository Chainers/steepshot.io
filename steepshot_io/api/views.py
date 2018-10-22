from rest_framework.generics import CreateAPIView

from steepshot_io.api import serializers


class WorkRequestAPIView(CreateAPIView):
    serializer_class = serializers.WorkRequestSerializer


class RequestAPIView(WorkRequestAPIView):
    serializer_class = serializers.RequestSerializer

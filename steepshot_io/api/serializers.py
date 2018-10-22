from django.conf import settings
from django.template.loader import render_to_string
from rest_framework import serializers

from steepshot_io.api.models import WorkRequest, DURATION_CHOICES, URGENCY_CHOICES
from steepshot_io.core.tasks import send_email


class WorkRequestSerializer(serializers.ModelSerializer):
    _emails = settings.WORK_REQUEST_EMAILS

    class Meta:
        model = WorkRequest
        fields = '__all__'

    def _send_email(self, data):
        duration = dict(DURATION_CHOICES).get(data.get('duration', ''))
        urgency = dict(URGENCY_CHOICES).get(data.get('urgency', ''))
        context = {
            'name': data.get('name', ''),
            'email': data.get('email', ''),
            'project_name': data.get('project_name', ''),
            'description': data.get('description', ''),
            'duration': duration,
            'urgency': urgency,
        }
        content = render_to_string('email.html', context)
        send_email.delay(content, self._emails)

    def save(self, **kwargs):
        instance = super(WorkRequestSerializer, self).save(**kwargs)
        self._send_email(self.data)
        return instance


class RequestSerializer(WorkRequestSerializer):
    _emails = ('b2b@p2p.org',)

    class Meta(WorkRequestSerializer.Meta):
        fields = ('name', 'email', 'description')

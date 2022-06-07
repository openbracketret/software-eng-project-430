from rest_framework import serializers


class APISerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        success = True
        payload = data
        if isinstance(data, dict):
            if 'success' in data:
                success = data.pop('success')
            if 'payload' in data:
                payload = data.pop('payload')
            if 'reason' in data:
                reason = data.get('reason')
                self.context['reason'] = data.get('reason')
        self.context['success'] = success

        return dict(
            self.context,
            **{'payload': payload}
        )
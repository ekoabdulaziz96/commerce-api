from rest_framework import serializers
import six


class RequestUserMixin(object):
    def get_current_user(self):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            return request.user
        return None


class BaseModelSerializer(serializers.ModelSerializer, RequestUserMixin):
    pass


class BaseSerializer(serializers.Serializer, RequestUserMixin):
    pass


class ChoiceDisplayField(serializers.ChoiceField):
    def __init__(self, *args, **kwargs):
        self.support_empty_key = kwargs.pop("support_empty_key", False)

        super().__init__(*args, **kwargs)
        self.choice_strings_to_display = {six.text_type(key): value for key, value in self.choices.items()}

    def to_representation(self, value):
        if not self.support_empty_key and value in ("", None):
            return None

        return {
            "value": self.choice_strings_to_values.get(six.text_type(value), value),
            "display_name": self.choice_strings_to_display.get(six.text_type(value), value),
        }

from rest_framework import viewsets 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
from .models import Trigger,Template 
from .serializers import TriggerSerializer , TemplateSerializer 
from .services import send_notification 

class TriggerViewSet(viewsets.ModelViewSet):
    queryset = Trigger.objects.all()
    serializer_class = TriggerSerializer 

    def perform_create(self, serializer):
        trigger = serializer.save()
        for channel, _ in Template.CHANNELS:
            Template.objects.create(trigger=trigger, channel=channel) 

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.all()
    serializer_class = TemplateSerializer 


@api_view(['POST'])
def fire_trigger(request):
    trigger_name = request.data.get('trigger_name')
    user_data = request.data.get('user_data')

    try:
        trigger = Trigger.objects.get(name__iexact = trigger_name)
        for template in trigger.templates.filter(is_active=True):
            send_notification(template.channel, template.content,user_data)
        return Response({"status":"Dispatched"})
    except Trigger.DoesNotExist:
        return Response({"error": "Trigger Not Found"}, status=404)

@api_view(["POST"])
def test_template(request, template_id):
    template = Template.objects.get(id=template_id)
    send_notification(template.channel, template.content, request.data.get('user_data'))
    return Response({"status": "Test sent"})
from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, Stage, StageChangeEvent
from .serializers import CustomerSerializer, StageSerializer, StageChangeEventSerializer
from . import utils
 
class CustomerViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing customer instances.
    """
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()   

class StageViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stage instances.
    """
    serializer_class = StageSerializer
    queryset = Stage.objects.all()   

class StageChangeEventViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing stagechangeevent instances.
    """
    serializer_class = StageChangeEventSerializer
    queryset = StageChangeEvent.objects.all()   

    # http://localhost:8000/api/stage-change-events/group_stage_change_events/
    @action(detail=False, methods=["POST"])
    def group_stage_change_events(self, request, pk=None):

        return Response(
            data=[], status=500
        )

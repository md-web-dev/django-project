from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Customer, Stage, StageChangeEvent, GroupStageChangeMapping
from .serializers import CustomerSerializer, StageSerializer, StageChangeEventSerializer, GroupStageChangeMappingSerializer
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
        mapping = request.data.get('mapping', None)
        stage_change_counts = utils.group_stage_change_event_counts(mapping)
        return Response(
            data=stage_change_counts, status=200
        )

class GroupStageChangeMappingViewSet(viewsets.ModelViewSet):

    serializer_class = GroupStageChangeMappingSerializer
    queryset = GroupStageChangeMapping.objects.all().order_by('id')
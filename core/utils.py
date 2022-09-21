from django.db.models import Count, F
from .models import StageChangeEvent
from convtools import conversion as c


def group_stage_change_converter(mapping):
    stage_change_events = StageChangeEvent.objects.select_related('stage').values(
        f_stage=F('from_stage__slug'), t_stage=F('to_stage__slug')).exclude(from_stage__isnull=True, to_stage__isnull=True)
    new_mapping = []
    for stage_change_event in stage_change_events:
        from_stage = mapping.get(stage_change_event.get('f_stage'), "None")
        to_stage = mapping.get(stage_change_event.get('t_stage'), "None")
        if not from_stage == to_stage:
            stage = {'from_stage': from_stage, "count": 1, "to_stage": to_stage}
            new_mapping.append(stage)

    converter = c.group_by(c.item('from_stage'), c.item('to_stage')).aggregate({
        "from_stage_name": c.item('from_stage'),
        "to_stage_name": c.item('to_stage'),
        "count_of_stage_changes": c.ReduceFuncs.Sum(c.item('count'))
    }).gen_converter()
    return converter(new_mapping)


def group_stage_change_event_counts(stage_mapping=None):
    if stage_mapping:
        return group_stage_change_converter(stage_mapping)
     
    stage_change_events = StageChangeEvent.objects.select_related('stage').values(
        from_stage_name=F('from_stage__name'), to_stage_name=F('to_stage__name')).annotate(count_of_stage_changes=Count('from_stage')).exclude(from_stage__isnull=True, to_stage__isnull=True)
    return list(stage_change_events)

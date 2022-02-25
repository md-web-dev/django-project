
import json
from pprint import pprint
from deepdiff import DeepDiff

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APITestCase

from core import utils

User = get_user_model()

EXPECTED_OUTPUT_WITHOUT_STAGE_MAPPING = [
    {
        "from_stage_name": "New Referral",
        "to_stage_name": "On Hold",
        "count_of_stage_changes": 10
    },
    {
        "from_stage_name": "New Referral",
        "to_stage_name": "Contacted",
        "count_of_stage_changes": 18
    },
    {
        "from_stage_name": "New Referral",
        "to_stage_name": "Scheduled",
        "count_of_stage_changes": 2
    },
    {
        "from_stage_name": "On Hold",
        "to_stage_name": "Contacted",
        "count_of_stage_changes": 12
    },
    {
        "from_stage_name": "Contacted",
        "to_stage_name": "Scheduled",
        "count_of_stage_changes": 25
    },
    {
        "from_stage_name": "Contacted",
        "to_stage_name": "Reviewed",
        "count_of_stage_changes": 2
    },
    {
        "from_stage_name": "Scheduled",
        "to_stage_name": "On Hold",
        "count_of_stage_changes": 2
    },
    {
        "from_stage_name": "Scheduled",
        "to_stage_name": "In Review",
        "count_of_stage_changes": 23
    },
    {
        "from_stage_name": "In Review",
        "to_stage_name": "Reviewed",
        "count_of_stage_changes": 21
    },
    {
        "from_stage_name": "Reviewed",
        "to_stage_name": "Complete",
        "count_of_stage_changes": 23
    },
    {
        "from_stage_name": "None",
        "to_stage_name": "New Referral",
        "count_of_stage_changes": 30
    }
]

STAGE_MAPPING_1 =  {
     "new_referral": "Scheduling",
     "on_hold": "Scheduling",
     "contacted": "Scheduling", 
     "scheduled": "Scheduling", 
     "in_review": "Review", 
     "reviewed": "Review", 
     "complete": "Complete",
     "cancelled": "Complete",
     "archived": "Complete"
 }

EXPECTED_OUTPUT_WITH_STAGE_MAPPING_1 = [
    {
        "from_stage_name": "None",
        "to_stage_name": "Scheduling",
        "count_of_stage_changes": 30
    },
    {
        "from_stage_name": "Scheduling",
        "to_stage_name": "Review",
        "count_of_stage_changes": 25
    },
    {
        "from_stage_name": "Review",
        "to_stage_name": "Complete",
        "count_of_stage_changes": 23
    }
]


STAGE_MAPPING_2 =  {
     "new_referral": "Processing",
     "on_hold": "Processing",
     "contacted": "Processing", 
     "scheduled": "Processing", 
     "in_review": "Processing", 
     "reviewed": "Processing",
     "complete": "Complete",
     "cancelled": "Cancelled",
     "archived": "Cancelled"
 }

EXPECTED_OUTPUT_WITH_STAGE_MAPPING_2 = [
    {
        "from_stage_name": "None",
        "to_stage_name": "Processing",
        "count_of_stage_changes": 30
    },
    {
        "from_stage_name": "Processing",
        "to_stage_name": "Complete",
        "count_of_stage_changes": 23
    }
]




class StageChangeTestCase(APITestCase):
    fixtures = ["fixtures/users.json", "fixtures/stages.json", "fixtures/customers.json", "fixtures/stage_change_events.json"]

    def assertUnorderedJsonEquivalence(self, first, second):
        deep_diff = DeepDiff(first, second, ignore_order=True)
        if deep_diff:
            pprint(deep_diff)
        self.assertEqual(deep_diff, {})

    def test_group_stage_change_event_counts_without_stage_mapping(self):
        self.assertUnorderedJsonEquivalence(
            utils.group_stage_change_event_counts(),
            EXPECTED_OUTPUT_WITHOUT_STAGE_MAPPING
        )

    def test_group_stage_event_counts(self):
        self.assertUnorderedJsonEquivalence(
            utils.group_stage_change_event_counts(STAGE_MAPPING_1),
            EXPECTED_OUTPUT_WITH_STAGE_MAPPING_1
        )

        self.assertUnorderedJsonEquivalence(
            utils.group_stage_change_event_counts(STAGE_MAPPING_2),
            EXPECTED_OUTPUT_WITH_STAGE_MAPPING_2
        )
    
    def test_post_group_stage_change_events_action(self):
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        response_without_mapping = self.client.post(
            '/api/stage-change-events/group_stage_change_events/', 
            {}, 
            format='json'
        )
        self.assertEqual( response_without_mapping.status_code, 200)
        self.assertUnorderedJsonEquivalence( 
            response_without_mapping.data, 
            EXPECTED_OUTPUT_WITHOUT_STAGE_MAPPING
        )

        response_without_mapping = self.client.post(
            '/api/stage-change-events/group_stage_change_events/', 
            {'mapping': STAGE_MAPPING_1}, 
            format='json'
        )
        self.assertEqual( response_without_mapping.status_code, 200)
        self.assertUnorderedJsonEquivalence( 
            response_without_mapping.data, 
            EXPECTED_OUTPUT_WITH_STAGE_MAPPING_1
        )



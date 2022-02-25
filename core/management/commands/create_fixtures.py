import random
import json
import datetime

from django.core.management.base import BaseCommand
from faker import Faker

fake = Faker()

STAGE_DATA = {
    "new_referral": "New Referral",
    "on_hold": "On Hold",
    "contacted": "Contacted",
    "scheduled": "Scheduled",
    "in_review": "In Review",
    "reviewed": "Reviewed",
    "complete": "Complete",
    "cancelled": "Cancelled",
    "archived": "Archived"
}

ALLOWED_STAGE_CHANGE_EVENT_PATHS = [
    ["new_referral", "contacted", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "on_hold", "contacted", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "on_hold", "contacted", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "contacted", "scheduled", "on_hold", "contacted", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "contacted" ],
    ["new_referral", "contacted", "scheduled"], 
    ["new_referral", "contacted", "scheduled", "in_review"],
    ["new_referral", "contacted", "scheduled"], 
    ["new_referral", "contacted", "on_hold", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "contacted", "reviewed", "complete"],
    ["new_referral", "contacted", "archived"],
    ["new_referral", "contacted", "scheduled", "in_review", "reviewed", "complete"],
    ["new_referral", "complete", "contacted", "scheduled", "in_review", "reviewed", "complete"],
]

ALLOWED_STAGE_CHANGE_EVENT_PATH_WEIGHTS = (25, 10, 10, 10, 7, 5, 5, 5, 5, 3, 2, 1, 1, 1)

def select_random_stage_change_path():
    return random.choices(ALLOWED_STAGE_CHANGE_EVENT_PATHS, weights=ALLOWED_STAGE_CHANGE_EVENT_PATH_WEIGHTS)[0]

def get_stage_id_from_slug(slug):
    return list(STAGE_DATA.keys()).index(slug) + 1

def write_stage_fixture():
    fixtures = []
    for slug, name in STAGE_DATA.items():
        fixture =   {
            "model": "core.stage",
            "pk": get_stage_id_from_slug(slug),
            "fields": {
                "name": name,
                "slug": slug,
                "created_at": "2021-11-15T20:21:35.282Z",
                "updated_at": "2021-11-15T20:21:35.282Z"
            }
        }
        fixtures.append(fixture)
    with open('fixtures/stages.json', 'w') as my_file:
        json.dump(fixtures, my_file)


def write_customer_and_stage_change_fixtures():

    customer_fixtures = []
    stage_change_fixtures = []
    stage_change_id = 0
    for c_i in range(30):
        customer_id = c_i + 1
        random_stage_change_path = select_random_stage_change_path()
        # print("random_stage_change_path", random_stage_change_path)
        last_stage_in_path = random_stage_change_path[-1]
        # print("last stage", last_stage_in_path)
        

        customer_current_stage_id = get_stage_id_from_slug(last_stage_in_path)
        # print("customer_current_stage_id", customer_current_stage_id)

        customer_created_at = fake.date_time_between_dates(
            datetime.datetime(2021, 11, 16, 20, 9, 35),
            datetime.datetime(2021, 12, 16, 20, 9, 35),
        )

        # reset this on the last stage change event creation
        customer_updated_at = None 
        stage_change_event_created_at = None

        # create the stage change events 
        # first so we can put each customer in the correct end stage
        for s_i, stage in enumerate(random_stage_change_path):
            if stage_change_event_created_at is None:
                stage_change_event_created_at = customer_created_at + datetime.timedelta(minutes=random.randint(0,14400))
            else:
                stage_change_event_created_at = stage_change_event_created_at + datetime.timedelta(minutes=random.randint(0,14400))
            stage_change_id = stage_change_id + 1
            stage_change_fixture =  {
                "model": "core.stagechangeevent",
                "pk": stage_change_id,
                "fields": {
                    "description": f"Moved from {STAGE_DATA[random_stage_change_path[s_i - 1]] if s_i > 0 else None} to {STAGE_DATA[stage]}",
                    "from_stage_id": get_stage_id_from_slug(random_stage_change_path[s_i - 1]) if s_i > 0 else None,
                    "to_stage_id": get_stage_id_from_slug(stage),
                    "customer": customer_id,
                    "created_at": stage_change_event_created_at.astimezone().isoformat(),
                    "updated_at": stage_change_event_created_at.astimezone().isoformat()
                }
            }
            stage_change_fixtures.append(stage_change_fixture)
            if s_i == len(random_stage_change_path) - 1:
                customer_updated_at = stage_change_event_created_at

        customer_fixture =     {
            "model": "core.customer",
            "pk": customer_id,
            "fields": {
                "name": fake.name(),
                "current_stage": customer_current_stage_id,
                "created_at": customer_created_at.astimezone().isoformat(),
                "updated_at": customer_updated_at.astimezone().isoformat()
            }
        }
        customer_fixtures.append(customer_fixture)


    with open('fixtures/stage_change_events.json', 'w') as my_file:
        json.dump(stage_change_fixtures, my_file)


    with open('fixtures/customers.json', 'w') as my_file:
        json.dump(customer_fixtures, my_file)

class Command(BaseCommand):
    help = "Seeds the db"

    def handle(self, *args, **options):
        write_stage_fixture()
        write_customer_and_stage_change_fixtures()






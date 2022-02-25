from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from thb_interview_project_events.users.api.views import UserViewSet
from core.views import CustomerViewSet, StageChangeEventViewSet, StageViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("customers", CustomerViewSet)
router.register("stage-change-events", StageChangeEventViewSet)
router.register("stages", StageViewSet)

app_name = "api"
urlpatterns = router.urls

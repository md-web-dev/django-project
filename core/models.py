from django.db import models


class TimestampMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, db_index=True)

    class Meta:
        abstract = True


class Customer(TimestampMixin, models.Model):
    name = models.CharField(max_length=800, null=True, blank=True)
    current_stage = models.ForeignKey(
        "Stage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='customer',
    )


class Stage(TimestampMixin, models.Model):
    name = models.CharField(max_length=500, null=True, blank=True) 
    slug = models.SlugField()


class StageChangeEvent(TimestampMixin, models.Model):
    description = models.TextField(null=True, blank=True)
    from_stage = models.ForeignKey(
        "Stage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="events_as_from_stage"
    )
    to_stage = models.ForeignKey(
        "Stage",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="events_as_to_stage"
    )
    customer = models.ForeignKey(
        "Customer",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="events",
    )

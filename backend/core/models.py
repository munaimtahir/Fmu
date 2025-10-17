from __future__ import annotations

from django.db import models


class TimeStampedModel(models.Model):
    """Reusable base model that tracks creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

    def touch(self, using: str | None = None, update_fields: set[str] | None = None) -> None:
        """Force an update to refresh the ``updated_at`` timestamp."""

        save_kwargs: dict[str, object] = {}
        if using:
            save_kwargs["using"] = using
        if update_fields is not None:
            save_kwargs["update_fields"] = update_fields
        self.save(**save_kwargs)

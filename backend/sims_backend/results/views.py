from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from sims_backend.common_permissions import IsAdminOrRegistrarReadOnlyFacultyStudent

from .models import PendingChange, Result
from .serializers import PendingChangeSerializer, ResultSerializer


class ResultViewSet(viewsets.ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["student__reg_no", "section__course__code", "final_grade"]
    ordering_fields = ["id", "published_at"]

    def update(self, request, *args, **kwargs):
        """Override update to prevent editing published results"""
        instance = self.get_object()
        if instance.is_published:
            return Response(
                {
                    "error": {
                        "code": 403,
                        "message": "Cannot edit published result. Use change-request endpoint instead.",
                    }
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Override partial_update to prevent editing published results"""
        instance = self.get_object()
        if instance.is_published:
            return Response(
                {
                    "error": {
                        "code": 403,
                        "message": "Cannot edit published result. Use change-request endpoint instead.",
                    }
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        return super().partial_update(request, *args, **kwargs)

    @action(detail=False, methods=["post"])
    def publish(self, request):
        """Publish a result (freeze it from direct edits)"""
        result_id = request.data.get("result_id")
        published_by = request.data.get("published_by", "")

        if not result_id:
            return Response(
                {"error": {"code": 400, "message": "result_id is required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = Result.objects.get(id=result_id)
        except Result.DoesNotExist:
            return Response(
                {"error": {"code": 404, "message": "Result not found"}},
                status=status.HTTP_404_NOT_FOUND,
            )

        if result.is_published:
            return Response(
                {"error": {"code": 400, "message": "Result is already published"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        result.is_published = True
        result.published_at = timezone.now()
        result.published_by = published_by
        result.save()

        serializer = self.get_serializer(result)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="change-request")
    def change_request(self, request):
        """Create a change request for a published result"""
        result_id = request.data.get("result_id")
        new_grade = request.data.get("new_grade")
        requested_by = request.data.get("requested_by", "")
        reason = request.data.get("reason", "")

        if not result_id or not new_grade:
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": "result_id and new_grade are required",
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = Result.objects.get(id=result_id)
        except Result.DoesNotExist:
            return Response(
                {"error": {"code": 404, "message": "Result not found"}},
                status=status.HTTP_404_NOT_FOUND,
            )

        if not result.is_published:
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": "Can only create change requests for published results",
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        pending_change = PendingChange.objects.create(
            result=result,
            new_grade=new_grade,
            requested_by=requested_by,
            reason=reason,
        )

        serializer = PendingChangeSerializer(pending_change)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=["post"], url_path="approve-change")
    def approve_change(self, request):
        """Approve or reject a change request"""
        change_id = request.data.get("change_id")
        approved = request.data.get("approved", False)
        approved_by = request.data.get("approved_by", "")

        if not change_id:
            return Response(
                {"error": {"code": 400, "message": "change_id is required"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            pending_change = PendingChange.objects.get(id=change_id)
        except PendingChange.DoesNotExist:
            return Response(
                {"error": {"code": 404, "message": "Change request not found"}},
                status=status.HTTP_404_NOT_FOUND,
            )

        if pending_change.status != "pending":
            return Response(
                {
                    "error": {
                        "code": 400,
                        "message": f"Change request is already {pending_change.status}",
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if approved:
            # Apply the change
            result = pending_change.result
            result.final_grade = pending_change.new_grade
            result.save()

            pending_change.status = "approved"
            pending_change.approved_by = approved_by
            pending_change.resolved_at = timezone.now()
            pending_change.save()

            return Response(
                {
                    "message": "Change approved and applied",
                    "result": ResultSerializer(result).data,
                    "change": PendingChangeSerializer(pending_change).data,
                }
            )
        else:
            # Reject the change
            pending_change.status = "rejected"
            pending_change.approved_by = approved_by
            pending_change.resolved_at = timezone.now()
            pending_change.save()

            return Response(
                {
                    "message": "Change rejected",
                    "change": PendingChangeSerializer(pending_change).data,
                }
            )


class PendingChangeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PendingChange.objects.all()
    serializer_class = PendingChangeSerializer
    permission_classes = [IsAuthenticated, IsAdminOrRegistrarReadOnlyFacultyStudent]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["result__student__reg_no", "status"]
    ordering_fields = ["id", "requested_at", "resolved_at"]

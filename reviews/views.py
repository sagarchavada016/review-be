from rest_framework import generics, status, filters
from utils.pagination import CustomPageNumberPagination
from .models import Freelancer, Review
from .serializers import FreelancerSerializer, ReviewSerializer
from rest_framework.response import Response
from django.db.models import Avg
from django.shortcuts import get_object_or_404


class AddFreelancerView(generics.ListCreateAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    pagination_class = CustomPageNumberPagination
    lookup_field = "id"
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "name"]
    search_fields = ["name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response("Freelancer", serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        response_data = {
            "message": "Freelancer Created Succesfully",
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class GetFreelancerByIDView(generics.RetrieveAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    lookup_field = "id"

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = {
            "message": "Freelancer Retrieved Successfully",
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)


class SubmitReviewView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["date", "rating","created_at"]
    search_fields = ["reviewer_name", "review_text"]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        uuid = self.kwargs["freelancer_id"]
        queryset = Review.objects.filter(freelancer=uuid)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response("Reviews", serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        freelancer_id = kwargs.get("freelancer_id")
        freelancer = get_object_or_404(Freelancer, id=freelancer_id)

        data = request.data.copy()
        data["freelancer"] = freelancer.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response_data = {
            "message": "Review Created Successfully",
            "success": True,
            "data": serializer.data,
        }
        return Response(response_data, status=status.HTTP_201_CREATED)


class GetFreelancerReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["date", "rating","created_at"]
    search_fields = ["reviewer_name", "review_text"]
    pagination_class = CustomPageNumberPagination

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.paginator.get_paginated_response("Reviews", serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


# class AverageRatingByFreelancerView(generics.GenericAPIView):
#     serializer_class = FreelancerSerializer
#     lookup_field = "id"

#     def get(self, request, *args, **kwargs):
#         freelancer_id = self.kwargs["id"]
#         freelancer = Freelancer.objects.get(id=freelancer_id)
#         average_rating = Review.objects.filter(freelancer=freelancer).aggregate(
#             Avg("rating")
#         )["rating__avg"]
#         response_data = {
#             "message": "Retrived Succesfully",
#             "success": True,
#             "data": {"freelancer": freelancer.name, "average_rating": average_rating},
#         }
#         return Response(response_data, status=status.HTTP_200_OK)


# class AverageRatingForAllReviewsView(generics.GenericAPIView):

#     def get(self, request, *args, **kwargs):
#         average_rating = Review.objects.aggregate(Avg("rating"))["rating__avg"]
#         response_data = {
#             "success": True,
#             "average_rating": average_rating,
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

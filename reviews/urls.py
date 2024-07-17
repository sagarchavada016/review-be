from django.urls import path
from .views import (
    AddFreelancerView,
    GetFreelancerReviewListView,
    SubmitReviewView,
    GetFreelancerByIDView,
)

urlpatterns = [
    ######################################################################
    path("freelancers/", AddFreelancerView.as_view(), name="freelancer-add"),
    path("freelancer/", AddFreelancerView.as_view(), name="freelancer-get"),
    path(
        "freelancers/<uuid:id>/",
        GetFreelancerByIDView.as_view(),
        name="freelancer-detail",
    ),
    ########################################################################
    path(
        "reviews/<uuid:freelancer_id>/",
        SubmitReviewView.as_view(),
        name="review-submit",
    ),
    path(
        "reviews/<uuid:freelancer_id>/",
        SubmitReviewView.as_view(),
        name="review-detail",
    ),
    path(
        "reviews/list/",
        GetFreelancerReviewListView.as_view(),
        name="freelancer-reviews",
    ),
]

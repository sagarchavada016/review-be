from django.urls import path
from .views import (
    AddFreelancerView,
    AverageRatingByFreelancerView,
    AverageRatingForAllReviewsView,
    GetFreelancerReviewListView,
    SubmitReviewView,
    GetFreelancerByIDView,
)

urlpatterns = [
    ######################################################################
    path("freelancer/", AddFreelancerView.as_view(), name="freelancer-add"),
    path("freelancers/", AddFreelancerView.as_view(), name="freelancer-get"),
    path(
        "freelancers/<uuid:id>/",
        GetFreelancerByIDView.as_view(),
        name="freelancer-detail",
    ),
    ########################################################################
    path(
        "review/<uuid:freelancer_id>/",
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
    path('freelancers/<uuid:id>/average-rating/', AverageRatingByFreelancerView.as_view(), name='average-rating-by-freelancer'),
    path('reviews/average-rating/', AverageRatingForAllReviewsView.as_view(), name='average-rating-for-all-reviews'),

]

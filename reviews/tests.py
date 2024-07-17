from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Review
from django.utils import timezone
from rest_framework import status
from django.urls import reverse


class ReviewModelTest(TestCase):

    def test_reviewer_name_blank(self):
        review = Review(
            reviewer_name="",
            rating=3,
            review_text="Good work!",
            freelancer="Freelancer1",
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_reviewer_name_max_length(self):
        review = Review(
            reviewer_name="a" * 101,
            rating=3,
            review_text="Good work!",
            freelancer="Freelancer1",
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_below_min(self):
        review = Review(
            reviewer_name="John Doe",
            rating=0,
            review_text="Bad work!",
            freelancer="Freelancer1",
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_above_max(self):
        review = Review(
            reviewer_name="John Doe",
            rating=6,
            review_text="Bad work!",
            freelancer="Freelancer1",
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_rating_not_integer(self):
        review = Review(
            reviewer_name="John Doe",
            rating="three",
            review_text="Bad work!",
            freelancer="Freelancer1",
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_review_text_blank(self):
        review = Review(
            reviewer_name="John Doe", rating=3, review_text="", freelancer="Freelancer1"
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_freelancer_blank(self):
        review = Review(
            reviewer_name="John Doe", rating=3, review_text="Good work!", freelancer=""
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_freelancer_max_length(self):
        review = Review(
            reviewer_name="John Doe",
            rating=3,
            review_text="Good work!",
            freelancer="a" * 256,
        )
        with self.assertRaises(ValidationError):
            review.full_clean()

    def test_submit_review_valid_data(self):
        url = reverse("submit-review")
        data = {
            "reviewer_name": "John Doe",
            "rating": 4,
            "review_text": "Great work!",
            "freelancer": "Freelancer1",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().reviewer_name, "John Doe")

    def test_submit_review_missing_fields(self):
        url = reverse("submit-review")
        data = {
            "reviewer_name": "John Doe",
            "rating": 4,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 0)

    def test_submit_review_invalid_rating(self):
        url = reverse("submit-review")
        data = {
            "reviewer_name": "John Doe",
            "rating": 6,
            "review_text": "Great work!",
            "freelancer": "Freelancer1",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 0)

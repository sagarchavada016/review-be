from rest_framework import serializers
from .models import Freelancer, Review
from django.db.models import Avg

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at", "deleted")


class FreelancerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "freelancer"]


class FreelancerSerializer(serializers.ModelSerializer):
    review_count = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        fields = ["id", "name", "review_count", "average_rating", "created_at"]

    def get_review_count(self, obj):
        return Review.objects.filter(freelancer=obj).count()
    
    def get_average_rating(self, obj):
        return Review.objects.filter(freelancer=obj).aggregate(Avg("rating"))["rating__avg"]

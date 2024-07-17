from rest_framework import serializers
from .models import Freelancer, Review


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

    class Meta:
        model = Freelancer
        fields = ["id", "name", "review_count",]

    def get_review_count(self, obj):
        return Review.objects.filter(freelancer=obj).count()

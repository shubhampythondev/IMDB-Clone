from rest_framework import serializers
from .models import Watchlist, StreamPlatform, Review


class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    watchlist = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = '__all__'
        execlude = ('watchlist')


class WatchlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watchlist
        fields = '__all__'

    def validate_name(self, value):
        if len(value) <= 2:
            raise serializers.ValidationError("Name is too short")
        return value


class StreamPlatformSerializer(serializers.ModelSerializer):
    # watchlist = serializers.StringRelatedField(many=True, read_only=True)
    # url = serializers.HyperlinkedIdentityField(view_name='Stream-platform-detail')

    watchlist = WatchlistSerializer(many=True, read_only=True)

    class Meta:
        model = StreamPlatform
        fields = '__all__'

# class WatchlistSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=60)
#     storyline = serializers.CharField(max_length=60)
#     # platform = serializers.ForeignKey(StreamPlatform, on_delete=models.CASCADE)
#     active = serializers.BooleanField(default=True)
#     created = serializers.DateTimeField()
#
#     def create(self, validated_data):
#         """Create and return a new `Watchlist` instance, given the validated data. """
#         return Watchlist.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         """
#         Update and return an existing `Watchlist` instance, given the validated data.
#         """
#         instance.title = validated_data.get('title', instance.title)
#         instance.storyline = validated_data.get('', instance.storyline)
#         instance.created = validated_data.get('created', instance.created)
#         instance.active = validated_data.get('active', instance.active)
#         instance.save()
#         return instance
#
#
# class StreamPlatformSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(max_length=60)
#     about = serializers.CharField(max_length=100)
#     website = serializers.URLField(max_length=100)

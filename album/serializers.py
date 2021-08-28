from accounts.serializers import UserBasicInfoSerializer
from core.settings import BASE_DIR
from django.db.models import Q
from rest_framework import serializers
from rest_framework.reverse import reverse

from .models import Album, Image


class AlbumListSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()
    creator = UserBasicInfoSerializer(read_only=True)

    class Meta:
        model = Album
        fields = ["id", "creator", "name", "url", "is_public", "created"]

    def get_url(self, obj):
        return reverse("album-detail", args=[obj.id], request=self.context["request"])


class AlbumCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Album
        fields = ["id", "name", "parent_album", "is_public"]


class AlbumSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    child_albums = serializers.SerializerMethodField()
    allowed_users = serializers.SerializerMethodField()
    # allowed_users = UserBasicInfoSerializer(many=True, read_only=True)
    parent_album = AlbumListSerializer(read_only=True)
    creator = UserBasicInfoSerializer(read_only=True)

    class Meta:
        model = Album
        fields = "__all__"
        read_only_fields = ["created", "allowed_users"]

    def get_allowed_users(self, obj):
        user = self.context["request"].user
        if user == obj.creator:
            return UserBasicInfoSerializer(obj.allowed_users, many=True).data

    def get_images(self, obj):
        images = obj.image_set.all()
        return ImageSerializer(images, many=True, context={"request": self.context["request"]}).data

    def get_child_albums(self, obj):
        user = self.context["request"].user
        if user.is_anonymous:
            albums = obj.album_set.filter(is_public=True)
        elif user == obj.creator:
            albums = obj.album_set.all()
        else:
            albums = obj.album_set.filter(Q(allowed_users__exact=user) | Q(is_public=True))
        return AlbumListSerializer(albums, many=True, context={"request": self.context["request"]}).data


class ImageSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    thumbnail_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Image
        exclude = ["image", "album"]

    def get_url(self, obj):
        request = self.context["request"]
        album_id = request.parser_context["kwargs"]["pk"]
        return reverse("album-images-detail", args=[album_id, obj.id], request=request)

    def get_thumbnail_url(self, obj):
        request = self.context["request"]
        album_id = request.parser_context["kwargs"]["pk"]
        return reverse("album-images-thumbnail", args=[album_id, obj.id], request=request)


class ImageUploadSerializer(ImageSerializer):
    class Meta(ImageSerializer.Meta):
        fields = ["image"]
        exclude = None


class ImageUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["id", "title"]

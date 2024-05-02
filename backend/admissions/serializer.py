from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Admissions, Category, User, Banner, Department, FAQ, Score, Answer, Question, School, Stream, \
    Comment


class BaseSerializer(ModelSerializer):
    image = serializers.SerializerMethodField(source='image')

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri("/static/%s" % obj.image.name)
            return "/%s" % obj.image.name


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AdmissionsSerializer(ModelSerializer):
    category = CategorySerializer(many=False)

    class Meta:
        model = Admissions
        fields = ['id', 'name', 'content', 'category', 'start_date', 'end_date', 'created_date', 'updated_date']


class AdmissionsSerializerDetail(AdmissionsSerializer):
    like = serializers.SerializerMethodField()

    def get_like(self, lesson):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return lesson.like_set.filter(active=True, user=request.user).exists()

    class Meta:
        model = AdmissionsSerializer.Meta.model
        fields = AdmissionsSerializer.Meta.fields + ['like']


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class BannerSerializer(BaseSerializer):
    category = CategorySerializer(many=True)

    class Meta:
        model = Banner
        fields = '__all__'


class SchoolSerializer(ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'


class StreamSerializer(ModelSerializer):
    class Meta:
        model = Stream
        fields = '__all__'


class DepartmentSerializer(BaseSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ScoreSerializer(BaseSerializer):
    class Meta:
        model = Score
        fields = '__all__'


class QuestionSerializer(ModelSerializer):
    user = UserSerializer(many=False)
    stream = StreamSerializer(many=False)

    class Meta:
        model = Question
        fields = '__all__'


class FAQSerializer(ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']

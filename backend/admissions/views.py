import datetime
import time
from pathlib import Path

import firebase_admin
from firebase_admin import db, credentials
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse
from oauth2_provider.views import ProtectedResourceView
from rest_framework import viewsets, permissions, generics, status, parsers
from rest_framework.response import Response
from .models import Admissions, Category, User, Banner, Department, FAQ, Score, Answer, Question, School, Stream, \
    Comment, Like
from rest_framework.decorators import action

from .paginator import AdmissionsPaginator, FAQPaginator
from .perms import OwnerPermission, UserPermission
from .serializer import BannerSerializer, SchoolSerializer, AdmissionsSerializer, StreamSerializer, CategorySerializer, \
    DepartmentSerializer, ScoreSerializer, QuestionSerializer, FAQSerializer, UserSerializer, CommentSerializer, \
    AdmissionsSerializerDetail
from backend.settings import EMAIL_HOST_USER
from backend.settings import BASE_DIR

config = {
    "apiKey": "AIzaSyD5dM-iOCY2NXVOjKmSJxI16Ldrgy5_GHU",
    "authDomain": "admission-663b7.firebaseapp.com",
    "databaseURL": "https://admission-663b7-default-rtdb.firebaseio.com",
    "projectId": "admission-663b7",
    "storageBucket": "admission-663b7.appspot.com",
    "messagingSenderId": "257069571322",
    "appId": "1:257069571322:web:4e75ef8ba07fecaa3a3d43",
}


# cred = credentials.Certificate("path/to/serviceAccountKey.json")
# firebase_admin.initialize_app(cred)


# firebase = pyrebase.initialize_app(config)
# authe = firebase.auth()
# database = firebase.database()


class MyProtectedView(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

def index(request):
    print(BASE_DIR / "path/to/serviceAccountKey.json")
    data = {
        "name": "name",
        "email": "email"
    }
    # ref = db.reference(url="https://admission-663b7-default-rtdb.firebaseio.com")
    # ref.child("messages/2/3").set(data)
    # print(ref.child("messages").get().keys())

    # for key in ref.get().keys():
    #     # Lấy tham chiếu đến tài liệu hiện tại
    #     doc_ref = ref.child(key)
    #     print(doc_ref.get())
    #
    #     # Duyệt qua từng key con (thuộc tính) trong tài liệu
    #     for child_key in doc_ref.get().keys():
    #         # In key con (thuộc tính)
    #         print(child_key)
    return render(request, 'index.html')


def test(request):
    name = request.POST.get('name')
    age = request.POST.get('age')
    return render(request, 'test.html', {
        'name': name,
        'age': age,
    })


class MessageViewSet(viewsets.ViewSet):

    @action(methods=["post"], detail=False)
    def send_message(self, request):
        user = request.user
        receiver = request.data.get('receiver')
        created_date = time.time()
        if user.is_staff:
            user = user.id
        else:
            user = receiver
        message = request.data.get('message')
        if user and message:
            ref = db.reference(url="https://admission-663b7-default-rtdb.firebaseio.com")
            data = {
                "user": user,
                "message": message,
                "created_date": created_date
            }
            ref.child("messages/" + str(receiver)).push(data)
            print(data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class BannerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer

    def get_queryset(self):
        q = Banner.objects.filter(active=True)
        return q


class SchoolViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


class AdmissionsViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = Admissions.objects.all()
    serializer_class = AdmissionsSerializerDetail
    pagination_class = AdmissionsPaginator

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        q = Admissions.objects.all()
        kw = self.request.query_params.get('kw')
        cate = self.request.query_params.get('cate')
        if kw:
            q = q.filter(name__icontains=kw)
        if cate:
            q = q.filter(category_id=cate)
        return q

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['get'])
    def get_each_cate(self, request):
        categories = Category.objects.all()
        kw = request.query_params.get('kw')
        cate = request.query_params.get('cate')
        if kw:
            categories = categories.filter(name__icontains=kw)
        if cate:
            categories = categories.filter(id=cate)
        ls = []
        for cate in categories:
            a = Admissions.objects.filter(category=cate).order_by('-created_date')[:5]
            if a:
                ls.extend(a)
        return Response(AdmissionsSerializer(ls, many=True, context={
            'request': request
        }).data, status=status.HTTP_200_OK)

    @action(methods=["post"], url_path="comments", detail=True)
    def add_comment(self, request, pk):
        comment = Comment.objects.create(user=request.user, admissions=self.get_object(),
                                         content=request.data.get('content'))
        comment.save()
        return Response(CommentSerializer(comment, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)

    @action(methods=["GET"], url_path="get_comments", detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.filter(active=True).order_by('-created_date')

        page = self.paginate_queryset(comments)

        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        return Response(CommentSerializer(comments, many=True).data, status=status.HTTP_200_OK)

    @action(methods=["post"], url_path="like", detail=True)
    def like(self, request, pk):
        like, create = Like.objects.get_or_create(user=request.user, admissions=self.get_object())
        if not create:
            like.active = not like.active
            like.save()

        return Response(AdmissionsSerializerDetail(self.get_object(), context={
            'request': request
        }).data, status=status.HTTP_200_OK)


class StreamViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer

    @action(methods=["POST"], url_path="question", detail=True)
    def add_question(self, request, pk):
        print(request.data.get('content'))
        question = Question.objects.create(user=request.user, stream=self.get_object(),
                                           content=request.data.get('content'))
        question.save()
        return Response(QuestionSerializer(question, context={
            'request': request
        }).data, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class DepartmentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ScoreViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Score.objects.all()
    serializer_class = ScoreSerializer


class QuestionViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class FAQViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    pagination_class = FAQPaginator

    def get_queryset(self):
        q = FAQ.objects.all()
        # kw = self.request.query_params.get('kw')
        # if kw:
        #     q = q.filter(question__icontains=kw)
        q = q.filter(active=True)
        return q

    @action(methods=['post'], detail=False)
    def create_faq(self, request):
        name = request.data.get('name')
        question = request.data.get('question')
        email = request.data.get('email')
        phone = request.data.get('phone')
        if question and name and email and phone:
            faq = FAQ.objects.create(question=question, name=name, email=email, phone=phone)
            faq.save()

            emails = User.objects.filter(is_staff=True).values('email')
            email_list = [email['email'] for email in emails]
            print(email_list)

            # Nội dung email
            subject = "Câu hỏi mới được tạo"
            message = f"Câu hỏi mới đã được tạo. \n" \
                      f"Nội dung câu hỏi: '{faq.question}'. \n" \
                      f"Vui lòng kiểm tra và duyệt tại đây: http://127.0.0.1:8000/admin/admissions/question/"

            # Gửi email
            send_mail(
                subject,
                message,
                EMAIL_HOST_USER,
                email_list,
                fail_silently=True,
            )

            return Response(FAQSerializer(faq).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True)
    def create_answer(self, request, pk):
        answer = request.data.get('answer')
        if answer and pk:
            faq = FAQ.objects.get(pk=pk)
            faq.answer = answer
            faq.active = True
            faq.save()
            return Response(FAQSerializer(faq).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView, generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.request.method == 'PATCH':
            self.permission_classes = [UserPermission]
            return super(UserViewSet, self).get_permissions()
        if self.action.__eq__('get_current'):
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current", detail=False)
    def get_current(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)

    @action(methods=['PATCH'], url_path="avatar", detail=False)
    def update_avatar(self, request):
        user = request.user
        user.avatar = request.data.get('avatar')
        user.save()
        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [OwnerPermission]

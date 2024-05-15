from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe

from .dao import count_admissions_by_cate, count_banner, count_admissions, ratio_admissions, current_admissions, \
    previous_admissions, count_user, ratio_banners
from .models import Admissions, Category, User, Banner, Department, FAQ, Score, Answer, Question, School, Stream, \
    Comment, Like

from datetime import date


class AdmissionsAppAdminSite(admin.AdminSite):
    site_header = "TƯ VẤN TUYỂN SINH"

    def get_urls(self):
        return [
            path('admissions-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        stats = count_admissions_by_cate()
        banner_on = count_banner()
        admissions = count_admissions()
        r_admissions = ratio_admissions()
        c_admissions = current_admissions()
        p_admissions = previous_admissions()
        users = count_user()
        r_banners = ratio_banners()
        return TemplateResponse(request, 'admin/stats_view.html', {
            'stats': stats,
            'banner_on': banner_on,
            'admissions': admissions,
            'r_admissions': r_admissions,
            'c_admissions': c_admissions,
            'p_admissions': p_admissions,
            'users': users,
            'r_banners': r_banners,
        })


class AdmissionsForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Admissions
        fields = '__all__'


class AdmissionsInlineAdmin(admin.StackedInline):
    model = Admissions
    pk_name = 'category'


class AdmissionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'start_date', 'end_date', 'active']
    search_fields = ['name', 'start_date', 'end_date', 'category__name']
    list_filter = ['name', 'start_date', 'end_date']

    form = AdmissionsForm


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    list_filter = ['name']

    inlines = [AdmissionsInlineAdmin, ]


class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'image']
    readonly_fields = ['img']

    def img(self, obj):
        if obj:
            return mark_safe(
                "<img src='/static/{url}' width='120' />".format(url=obj.image.name)
            )

    class Media:
        css = {
            'all': ('/static/css/style.css',)
        }


class DepartmentForm(forms.ModelForm):
    introduction = forms.CharField(widget=CKEditorUploadingWidget)
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Department
        fields = '__all__'


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active']

    form = DepartmentForm


class StreamForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        model = Stream
        fields = '__all__'


class StreamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'active', 'start_time']

    form = StreamForm


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'content']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'user']
    search_fields = ['user']


admin_site = AdmissionsAppAdminSite(name="myapp")
# Register your models here.
admin_site.register(Admissions, AdmissionsAdmin)
admin_site.register(Category, CategoryAdmin)
admin_site.register(User)
admin_site.register(Banner, BannerAdmin)
admin_site.register(Department, DepartmentAdmin)
admin_site.register(FAQ)
admin_site.register(Score)
admin_site.register(Answer)
admin_site.register(Question, QuestionAdmin)
admin_site.register(School)
admin_site.register(Stream, StreamAdmin)
admin_site.register(Comment, CommentAdmin)
admin_site.register(Like)

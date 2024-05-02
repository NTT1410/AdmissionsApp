from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib import admin
from django.template.response import TemplateResponse
from django.urls import path
from django.utils.html import mark_safe

from .dao import count_admissions_by_cate
from .models import Admissions, Category, User, Banner, Department, FAQ, Score, Answer, Question, School, Stream, Comment, Like


class AdmissionsAppAdminSite(admin.AdminSite):
    site_header = "TƯ VẤN TUYỂN SINH"

    def get_urls(self):
        return [
            path('admissions-stats/', self.stats_view)
        ] + super().get_urls()

    def stats_view(self, request):
        stats = count_admissions_by_cate()
        return TemplateResponse(request, 'admin/stats_view.html', {
            'stats': stats
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
    list_display = ['id', 'name', 'status', 'content']
    search_fields = ['name']


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
admin_site.register(Comment)
admin_site.register(Like)

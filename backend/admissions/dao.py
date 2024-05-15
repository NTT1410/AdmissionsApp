import datetime
from datetime import date

from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.utils import timezone

from .models import Category, Admissions, Banner, User


def load_course(params={}):
    q = Admissions.objects.all()
    kw = params.get('kw')
    if kw:
        q = q.objects.filter(name__icontains=kw)
    cate = params.get('cate')
    if cate:
        q = q.objects.filter(category_id=cate)


def count_admissions_by_cate():
    return Category.objects.annotate(count=Count('admissions__id')).values('id', 'name', 'count').order_by('-id')


def count_banner():
    banner_on = Banner.objects.filter(active=True).annotate(count=Count('id')).values('id', 'name', 'count').order_by(
        '-id')
    return banner_on


def ratio_banners():
    now = timezone.now()
    current_year = now.year
    current_month = now.month

    # Tính số lượng banner của tháng hiện tại
    current_month_banners = Banner.objects.filter(created_date__year=current_year,
                                                  created_date__month=current_month).count()

    # Tính số lượng banner của tháng trước
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    previous_month_banners = Banner.objects.filter(created_date__year=previous_year,
                                                   created_date__month=previous_month).count()

    # Tính tỷ lệ tăng giảm
    if previous_month_banners == 0:
        if current_month_banners == 0:
            change_rate = 0  # Không có thay đổi nếu cả hai tháng đều là 0
        else:
            change_rate = 100  # Nếu tháng trước là 0 và tháng hiện tại có giá trị, tỷ lệ tăng là 100%
    else:
        change_rate = ((current_month_banners - previous_month_banners) / previous_month_banners) * 100

    return {
        'current_month_banners': current_month_banners,
        'previous_month_banners': previous_month_banners,
        'change_rate': change_rate
    }


def count_admissions():
    adm = Admissions.objects.filter(active=True).annotate(count=Count('id')).values('id', 'name', 'count').order_by(
        '-id')
    return adm


def current_month():
    return date.today()


def previous_month():
    return date.today().replace(day=1) - date.resolution


def ratio_admissions():
    now = timezone.now()
    current_year = now.year
    current_month = now.month

    # Tính số lượng Admissions của tháng hiện tại
    current_month_admissions = Admissions.objects.filter(created_date__year=current_year,
                                                  created_date__month=current_month).count()

    # Tính số lượng Admissions của tháng trước
    if current_month == 1:
        previous_month = 12
        previous_year = current_year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    previous_month_admissions = Admissions.objects.filter(created_date__year=previous_year,
                                                   created_date__month=previous_month).count()

    # Tính tỷ lệ tăng giảm
    if previous_month_admissions == 0:
        if current_month_admissions == 0:
            change_rate = 0  # Không có thay đổi nếu cả hai tháng đều là 0
        else:
            change_rate = 100  # Nếu tháng trước là 0 và tháng hiện tại có giá trị, tỷ lệ tăng là 100%
    else:
        change_rate = ((current_month_admissions - previous_month_admissions) / previous_month_admissions) * 100

    return change_rate


def current_admissions():
    c = date.today()
    return Admissions.objects.filter(created_date__year=c.year,
                                     created_date__month=c.month).count()


def previous_admissions():
    p = date.today().replace(day=1) - date.resolution
    return Admissions.objects.filter(created_date__year=p.year,
                                     created_date__month=p.month).count()


def count_user():
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    # Lấy danh sách số lượng user theo tháng
    user_counts = (
        User.objects.filter(date_joined__year=current_year, date_joined__month__lte=current_month)
        .annotate(month=TruncMonth('date_joined'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )

    # Tạo dictionary với các tháng và số lượng người dùng mặc định là 0
    month_counts = {month: 0 for month in range(1, current_month + 1)}

    # Điền số lượng người dùng vào dictionary
    for entry in user_counts:
        month_counts[entry['month'].month] = entry['count']

    # Chuyển dictionary sang danh sách tuple (tháng, số lượng)
    result = [{'month': datetime.date(current_year, month, 1), 'count': count} for month, count in month_counts.items()]

    return result

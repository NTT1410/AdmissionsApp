from rest_framework.pagination import PageNumberPagination


class AdmissionsPaginator(PageNumberPagination):
    page_size = 10


class FAQPaginator(PageNumberPagination):
    page_size = 25

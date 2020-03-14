from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination


class MyPagination(PageNumberPagination):
    page_size = 10
    page_query_param = "currentPage"
    page_size_query_param = "pageSize"
    max_page_size = 40



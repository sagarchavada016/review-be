from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "limit"
    max_page_size = 100
    skip_query_param = "skip"

    def paginate_queryset(self, queryset, request, view=None):
        limit = self.get_page_size(request)
        skip = request.query_params.get(self.skip_query_param, 0)

        try:
            skip = int(skip)
        except ValueError:
            skip = 0

        if skip < 0:
            raise NotFound("Skip parameter cannot be negative")

        self.count = queryset.count()
        self.limit = limit
        self.offset = skip
        self.request = request

        if self.count == 0 or skip >= self.count:
            return []

        return list(queryset[skip : skip + limit])

    def get_paginated_response(self, message, data):
        return Response(
            {
                "success": True,
                "message": f"{message} retrieved successfully",
                "data": {
                    "totalRecords": self.count,
                    "totalFilterRecords": len(data),
                    "result": data,
                },
            }
        )

    # def get_next_link(self):
    #     if self.offset + self.limit >= self.count:
    #         return None
    #     url = self.request.build_absolute_uri()
    #     return replace_query_param(url, self.skip_query_param, self.offset + self.limit)

    # def get_previous_link(self):
    #     if self.offset == 0:
    #         return None
    #     url = self.request.build_absolute_uri()
    #     return replace_query_param(url, self.skip_query_param, max(self.offset - self.limit, 0))

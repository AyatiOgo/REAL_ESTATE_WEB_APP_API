from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 2
    page_query_param = 'page'
    
    def get_paginated_response(self, data):
        return Response(  
            {
                'next' : self.get_next_link(),
                'prev' : self.get_previous_link(),
                'count' : self.page.paginator.count,
                'page_size' : self.page_size,
                'results' : data,
            }
        )
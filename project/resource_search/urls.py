from django.conf.urls import url
from resource_search.views import ResourceSearchAPIView

url(r'^$', ResourceSearchAPIView.as_view(), name='retrieve_order_details')
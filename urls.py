from rest_framework import routers

urlpatterns = [
    url(r'^share-redirect-url/(?P<slug>[-\w]+)/$', RichSocialShare.as_view(), name='rich_share_redirect'),
]

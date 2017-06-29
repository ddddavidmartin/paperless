from django.conf import settings
from django.conf.urls import url, static, include
from django.contrib import admin
from django.views.decorators.csrf import csrf_exempt

from rest_framework.routers import DefaultRouter

from documents.views import (
    FetchView, InlineView, PushView, ThumbnailView,
    CorrespondentViewSet, TagViewSet, DocumentViewSet, LogViewSet
)
from reminders.views import ReminderViewSet

router = DefaultRouter()
router.register(r"correspondents", CorrespondentViewSet)
router.register(r"documents", DocumentViewSet)
router.register(r"logs", LogViewSet)
router.register(r"reminders", ReminderViewSet)
router.register(r"tags", TagViewSet)

urlpatterns = [

    # API
    url(
        r"^api/auth/",
        include('rest_framework.urls', namespace="rest_framework")
    ),
    url(r"^api/", include(router.urls, namespace="drf")),

    # File downloads
    url(
        r"^fetch/(?P<kind>doc)/(?P<pk>\d+)$",
        FetchView.as_view(),
        name="fetch"
    ),

    # Inline file view
    url(
        r"^view/(?P<kind>doc)/(?P<pk>\d+)$",
        InlineView.as_view(),
        name="view"
    ),

    # Thumbnail view
    url(
        r"^fetch/(?P<kind>thumb)/(?P<pk>\d+)$",
        ThumbnailView.as_view(),
        name="thumbnail"
    ),

    # File uploads
    url(r"^push$", csrf_exempt(PushView.as_view()), name="push"),

    # The Django admin
    url(r"admin/", admin.site.urls),
    url(r"", admin.site.urls),  # This is going away

] + static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Text in each page's <h1> (and above login form).
admin.site.site_header = 'Paperless'
# Text at the end of each page's <title>.
admin.site.site_title = 'Paperless'
# Text at the top of the admin index page.
admin.site.index_title = 'Paperless administration'

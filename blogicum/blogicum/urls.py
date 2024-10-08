from django.conf.urls.static import static
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib import admin
from django.urls import include, path, reverse_lazy
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("pages/", include("pages.urls", namespace="pages")),
    path("", include("blog.urls", namespace="blog")),
    path("auth/", include("django.contrib.auth.urls")),
    path(
        "auth/registration/",
        CreateView.as_view(
            template_name="registration/registration_form.html",
            form_class=UserCreationForm,
            success_url=reverse_lazy("login"),
        ),
        name="registration",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += (path("__debug__/", include(debug_toolbar.urls)),)

handler403 = "pages.views.csrf_failure"
handler404 = "pages.views.page_not_found"
handler500 = "pages.views.custom_error_view"

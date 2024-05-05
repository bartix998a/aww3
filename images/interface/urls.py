from django.urls import path

from . import views

app_name = "interface"
urlpatterns = [
    path("", views.index, name="index"),
	path("authenticate", views.log, name="log"),
	path("site", views.service, name="site"),
	path("page/<int:page_no>", views.page, name="page"),
	path("site/<int:img_id>", views.picture, name="picture"),
	path("edit/<int:img_id>", views.edit, name="edit"),
	path("edit/remove_rect/<int:rect_id>", views.remove_rect, name="rmv_rect"),
	path("edit/add", views.add_rect, name="add_rect"),
	path("page/filter/<int:page_no>", views.filter, name="filter")
]
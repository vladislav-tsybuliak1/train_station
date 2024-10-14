from django.urls import path

from user_api.views import CreateUserView, ManageUserView


urlpatterns = [
    path("register/", CreateUserView.as_view(), name="create"),
    path("me/", ManageUserView.as_view(), name="manage"),
]

app_name = "user_api"

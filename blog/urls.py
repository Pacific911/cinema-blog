from django.urls import path
from .views import home,signup,login,dashboard,logout,new_blog,edit_blog,delete_blog,blogs,search_post,blog_details,new_team


urlpatterns = [
    path("", home, name="home"),
    path("signup", signup, name="register"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),

    # user dasboard paths
    path("dashboard", dashboard, name="dashboard"),
    path("create-blog", new_blog, name="create-blog"),
    path("new-team", new_team, name="new-team"),



    # Client view paths
    path("blogs", blogs, name="blogs"),
    path("update_blog/<int:by>", edit_blog, name="update_blog"),
    path("blog_delete/<int:by>", delete_blog, name="blog_delete"),
    path("blogs", blogs, name="blogs"),
    path("search", search_post, name="search"),
    path("blog_details/<int:by>", blog_details, name="blog_details"),

]

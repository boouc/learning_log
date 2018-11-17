"""定义learning_logs的URL模式"""

from django.urls import path

from . import views

app_name = "learning_logs"
urlpatterns = [
    # 主页
    path("", views.index, name="index"),

    # 显示所有主题的页面
    path("topics/", views.topics, name="topics"),

    # 特定主题的详细页面
    path("topics/<int:topic_id>/", views.topic, name="topic"),

    # 用户添加新主题的网页
    path("new_topic/", views.new_topic, name="new_topic"),

    # 用户添加新条目的页面, 条目要与指定的主题相关联
    path("new_entry/<int:topic_id>/", views.new_entry, name="new_entry"),

    # 用户编辑条目的页面
    path("edit_entry/<int:entry_id>/", views.edit_entry, name="edit_entry"),
]

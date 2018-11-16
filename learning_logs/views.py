from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Topic
from .forms import EntryForm, TopicForm


def index(request):
    """学习笔记的主页"""
    return render(request, "learning_logs/index.html")


def topics(request):
    """显示所有主题的页面"""
    topics = Topic.objects.order_by("date_added")
    context = {"topics": topics}  # 发送给模板的上下文, 数据
    return render(request, "learning_logs/topics.html", context)


def topic(request, topic_id):
    """显示单个主题及其所有条目"""
    topic = Topic.objects.get(id=topic_id)
    print(topic_id)
    entries = topic.entry_set.order_by("-date_added")  # date_added前面的减号表示降序
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


def new_topic(request):
    """添加新主题"""
    if request.method != "POST":
        # 未提交数据: 创建新主题
        form = TopicForm()
    else:
        # 对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("learning_logs:topics"))
            # reverse()获取指定页面的URL
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # commit=False表示不保存到数据库
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse("learning_logs:new_topic", args=[topic_id]))
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)

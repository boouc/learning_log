from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Entry, Topic
from .forms import EntryForm, TopicForm


def check_topic_owner(request, topic):
    """检查主题的所属用户是否为当前用户"""
    return topic.owner == request.user


def index(request):
    """学习笔记的主页"""
    return render(request, "learning_logs/index.html")


@login_required
def topics(request):
    """显示所有主题的页面"""
    # 只允许用户访问自己的主题
    topics = Topic.objects.filter(owner=request.user).order_by("date_added")
    context = {"topics": topics}  # 发送给模板的上下文, 数据
    return render(request, "learning_logs/topics.html", context)


@login_required
def topic(request, topic_id):
    """显示单个主题及其所有条目"""
    topic = get_object_or_404(Topic, id=topic_id)
    # 确认请求的主题属于当前用户
    if not check_topic_owner(request, topic):
        raise Http404

    entries = topic.entry_set.order_by("-date_added")  # date_added前面的减号表示降序
    context = {"topic": topic, "entries": entries}
    return render(request, "learning_logs/topic.html", context)


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != "POST":
        # 未提交数据: 创建新主题
        form = TopicForm()
    else:
        # 对数据进行处理
        form = TopicForm(request.POST)
        if form.is_valid():
            # 将新添加的主题关联到当前用户
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return HttpResponseRedirect(reverse("learning_logs:topics"))
            # reverse()获取指定页面的URL
    context = {"form": form}
    return render(request, "learning_logs/new_topic.html", context)


@login_required
def new_entry(request, topic_id):
    """在特定的主题中添加新条目"""
    topic = Topic.objects.get(id=topic_id)
    # 核实主题属于当前用户
    if not check_topic_owner(request, topic):
        raise Http404

    if request.method != "POST":
        form = EntryForm()
    else:
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)  # commit=False表示不保存到数据库
            new_entry.topic = topic
            new_entry.save()
            return HttpResponseRedirect(
                reverse("learning_logs:topic", args=(topic_id,)))
    context = {"topic": topic, "form": form}
    return render(request, "learning_logs/new_entry.html", context)


@login_required
def edit_entry(request, entry_id):
    """编辑指定的条目"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    # 确定主题和条目属于发送请求的用户
    if not check_topic_owner(request, topic):
        raise Http404

    if request.method != "POST":
        # 使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse("learning_logs:topic", args=(topic.id,)))

    context = {"entry": entry, "topic": topic, "form": form}
    return render(request, "learning_logs/edit_entry.html", context)

from django import forms

from .models import Entry, Topic


class TopicForm(forms.ModelForm):
    class Meta:
        # 根据模型创建表单, 确定表单的字段
        model = Topic
        fields = ["text"]
        # 让Django不要为text字段生成标签
        labels = {"text": ""}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["text"]
        labels = {"text": ""}
        widgets = {"text": forms.Textarea(attrs={"cols": 80})}

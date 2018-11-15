from django.contrib import admin

from learning_logs.models import Topic, Entry

admin.site.register(Topic)  # 将模型Topic注册到管理网站
admin.site.register(Entry)

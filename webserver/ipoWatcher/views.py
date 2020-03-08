from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("ipoWatcher 每日分析科创板新上信息, 搜索关键字发邮件, 暂不开放注册.")

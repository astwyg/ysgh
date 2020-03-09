from django.shortcuts import render
from django.http import HttpResponse
import time

from reportAna.src.find_keywords import find_keyword

def index(req):
    context = {}
    if req.method == "POST":
        return HttpResponse("整啥呢? 不允许POST")
    else:
        keywords = req.GET.get("keywords")
        path = req.GET.get("path")
        if keywords and path:
            time.sleep(5)
            msg = find_keyword(keywords, path)
            context["msg"] = msg or "未找到"
        return render(req, 'reportAna/find_keywords.html', context)

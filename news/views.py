from django.shortcuts import render
from .models import News

# Create your views here.
def news(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'news.html', {'news': news})
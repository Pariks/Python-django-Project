from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from news.models import Article
from followpost.models import Comments
from boc.forms import PostForm
import datetime
from django.utils import timezone
from django.http import HttpResponseRedirect, HttpResponse


def index(request):
    articles = Article.objects.filter(published=True).order_by('-date_published')
    articles_recent = articles[:10]
    articles_past = articles[11:]
    c = {'articles':articles, 'articles_recent':articles_recent, 'articles_past':articles_past}
    return render(request, 'news/all.html', c)
    

def article(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article_id = getattr(article,'id')
    comments = Comments.objects.filter(article_id = article_id)
    comments_number = comments.count()
    form = PostForm()
    c = {'article': article, 'comments':  comments,
            'comments_number':  comments_number, 'PostForm':  form}
    return render(request, 'news/article.html', c)                                                                                                                                                                                                                             
def comment(request, slug):
    article = get_object_or_404(Article, slug=slug)
    article_id = getattr(article,'id')
    if request.method == 'POST':
       form = PostForm(request.POST)
       if form.is_valid():
          comment = form.save(commit=False)
          comment.commented_by = request.user
          comment.article = article
          comment.save()
       else:
          return HttpResponse(form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
def comment_replies(request, slug, comment_id):
    article = get_object_or_404(Article, slug=slug)
    article_id = getattr(article,'id')
    comment = Comments.objects.get(id=comment_id)
    if request.method == 'POST':
       form = PostForm(request.POST)
       if form.is_valid():
          comments_obj = form.save(commit=False)
          comments_obj.commented_by = request.user
          comments_obj.article = article
          comments_obj.parent = comment
          comments_obj.save()
       else:
          return HttpResponse(form.errors)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

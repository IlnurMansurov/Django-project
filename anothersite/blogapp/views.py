"""
Модуль содерждит различные наборы представлений.

View блога пользователя.

"""
from django.contrib.gis.feeds import Feed
from django.urls import reverse_lazy, reverse

from .models import Article
from django.views.generic import ListView, DetailView
class ArticlesListView(ListView):
    queryset = (
        Article.objects
        .filter(published_at__isnull=False)
        .order_by('-published_at')
    )
class ArticleDetailView(DetailView):
    model = Article

class LatestArticlesField(Feed):
    title = 'Blog articles(latest)'
    description = 'Updates on changes and addition blog articles'
    link = reverse_lazy('blogapp:articles')

    def items(self):
        return (
           Article.objects
           .filter(published_at__isnull=False)
           .order_by('-published_at')[:5]
        )
    def item_title(self, item: Article):
        return item.title

    def item_description(self, item: Article):
        return item.body[:200]

    def item_link(self, item: Article):
        return reverse('blogapp:article', kwargs={'pk': item.pk})

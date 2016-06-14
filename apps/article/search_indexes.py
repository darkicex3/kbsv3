# from haystack import indexes
# from apps.article.models import Article, Tag, UserArticle, DailyRecap, User, Group, Category
#
#
# class CategoryIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     name = indexes.CharField(model_attr='name')
#
#     def get_model(self):
#         return Category
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.order_by('name')
#
#
# class UserArticleIndex (indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#     user_id = indexes.IntegerField(model_attr='user_id')
#     article_id = indexes.IntegerField(model_attr='article_id')
#     favorites = indexes.BooleanField(model_attr='favorites')
#     visited = indexes.BooleanField(model_attr='visited')
#     searched = indexes.BooleanField(model_attr='searched')
#     date_visited = indexes.DateTimeField(model_attr='date_visited')
#     date_searched = indexes.DateTimeField(model_attr='date_searched')
#     date_added = indexes.DateTimeField(model_attr='date_added')
#
#     def get_model(self):
#         return UserArticle
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.order_by('user_id')
#
#
# class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
#
#     text = indexes.CharField(document=True, use_template=True)
#     title = indexes.CharField(model_attr='title')
#     author = indexes.CharField(model_attr='author')
#     status = indexes.CharField(model_attr='status')
#
#     is_public = indexes.BooleanField(model_attr='is_public')
#     useful_counter = indexes.IntegerField(model_attr='useful_counter')
#     favorite_counter = indexes.IntegerField(model_attr='favorite_counter')
#     view_counter = indexes.IntegerField(model_attr='view_counter')
#     essential = indexes.BooleanField(model_attr='essential')
#
#     content = indexes.CharField(model_attr='content')
#     tags = indexes.MultiValueField()
#
#     publish_date = indexes.DateTimeField(model_attr='publish_date')
#     modified = indexes.DateTimeField(model_attr='modified')
#
#     title_auto = indexes.EdgeNgramField(model_attr='title')
#     # content_auto_content = indexes.EdgeNgramField(model_attr='content')
#     # content_auto_description = indexes.EdgeNgramField(model_attr='description')
#
#     def prepare_title_auto(self, obj):
#         return obj.title.lower()
#
#     def prepare_tags(self, obj):
#         return [tag.pk for tag in obj.tags.all()]
#
#     def get_model(self):
#         return Article
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.all()
#

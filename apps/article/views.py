import os
from datetime import datetime, timedelta
from django.utils import timezone

import simplejson as json
from attachments.models import Attachment
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import View

# from haystack.query import SearchQuerySet

from apps.article.models import Tag, Article, Category, Feedback, DailyRecap
from apps.poll.models import Poll, Choice

tf_ext = ["doc", "docx", "odt", "txt", "pages", "wps", "wpd", "msg", "log"]
df_ext = ["csv", "ppt", "pptx", "sdf", "tar", "xml", "vcf", "dat", "key"]
af_ext = ["aif", "iff", "m3u", "m4a", "mid", "mp3", "mpa", "wav", "wma"]
vf_ext = ["3g2", "3gp", "asf", "avi", "flv", "m4v", "mov", "mp4", "mpg", "rm", "srt", "swf", "vob", "wmv"]
rif_ext = ["bmp", "gif", "jpg", "png", "psd", "pspimage", "tif", "tiff", "yuv", "thm"]
plf_ext = ["indd", "pct", "pdf"]
sf_ext = ["xlr", "xls", "xlsx"]
cf_ext = ["zip", "rar", "pkg", "7z"]


@login_required
def index_search(request):
    return render(request, 'article/base.html')


@login_required
def articles_search(request):
    tags = request.GET.get('in')
    sort = request.GET.get('by')

    suggestions = []

    # sqs = SearchQuerySet().autocomplete(title_auto__startswith=request.GET.get('q'))
    sqs = Article.objects.filter(title__startswith=request.GET.get('q'))
    # if sort != '':
    #     sqs.order_by(sort)

    if tags != '':
        tag = Tag.objects.get(name=tags)
        for i in sqs:
            for a in i.tags:
                tmp = Tag.objects.get(pk=a)
                if tmp.name == tag.name:
                    suggestions.append(i.title)
    else:
        suggestions = [result.pk for result in sqs]

    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')


class IncrementCounterTags(View):
    def get(self, *args, **kwargs):
        context = {}
        tag_name = self.request.GET.get('in')
        tag = Tag.objects.get(name=tag_name)
        tag.click_counter += 1
        tag.save()
        return JsonResponse(context)


class GetCategoriesView(View):
    @login_required
    def get(self, *args, **kwargs):

        context = {}
        node_id = self.request.GET.get('node_id')
        previous = self.request.GET.get('previous')

        if node_id is None:
            tags = Tag.objects.all().filter(level=0)
        else:
            node_category = Tag.objects.all().get(pk=node_id)
            if previous == 'false':
                tags = node_category.get_children()
            else:
                tags = node_category.get_previous_parent().get_children()

        for tag in tags:
            context.update({tag.id: str(tag.name)})

        return JsonResponse(context)


class SetLikedView(View):
    def get(self, *args, **kwargs):
        context = {}

        article_id = self.request.GET.get('id')
        action = self.request.GET.get('action')
        q = Article.objects.get(id=article_id)
        user = self.request.user

        if user.username not in q.users_likes.values_list('username', flat=True):
            q.users_likes.add(user)
            q.favorite_counter += 1
        else:
            q.users_likes.remove(user)
            q.favorite_counter -= 1

        q.save()

        context.update({'favorite_counter': q.favorite_counter})
        return JsonResponse(context)


class SetUsefulView(View):
    def get(self, *args, **kwargs):
        context = {}

        article_id = self.request.GET.get('id')
        action = self.request.GET.get('action')
        q = Article.objects.get(id=article_id)
        user = self.request.user

        if user.username not in q.users_bigup.values_list('username', flat=True):
            q.users_bigup.add(user)
            q.useful_counter += 1
        else:
            q.users_bigup.remove(user)
            q.useful_counter -= 1

        q.save()

        context.update({'useful_counter': q.useful_counter})
        return JsonResponse(context)


class SetReadView(View):
    def get(self, *args, **kwargs):
        context = {}

        article_id = self.request.GET.get('id')
        q = Article.objects.get(id=article_id)
        user = self.request.user
        q.view_counter += 1
        q.save()

        return JsonResponse(context)


class SetVisitedView(View):
    def get(self, *args, **kwargs):
        context = {}

        # article_id = self.request.GET.get('id')
        # user = self.request.user
        #
        # try:
        #     p = UserArticle.objects.all().get(user_id=user.id, article_id=article_id)
        #     p.visited = True
        #     p.date_visited = datetime.datetime.now()
        #     p.save()
        #
        # except ObjectDoesNotExist:
        #     UserArticle.objects.create(user_id=user.id, article_id=article_id, visited=True,
        #                                date_visited=datetime.datetime.now())

        return JsonResponse(context)


class SetSearchedView(View):
    def get(self, *args, **kwargs):
        context = {}

        # article_id = self.request.GET.get('article_id')
        # user = self.request.user
        #
        # try:
        #     p = UserArticle.objects.all().get(user_id=user.id, article_id=article_id)
        #     p.searched = True
        #     p.date_searched = datetime.datetime.now()
        #     p.save()
        #
        # except ObjectDoesNotExist:
        #     UserArticle.objects.create(user_id=user.id, article_id=article_id, searched=True,
        #                                date_searched=datetime.datetime.now())

        return JsonResponse(context)


class CreateShortcutView(View):
    @login_required
    def get(self, *args, **kwargs):
        context = {}
        shortcut_name = self.request.GET.get('shortcut_name')
        category = Category.objects.create(name=shortcut_name)

        if category:
            context['success'] = True

        return JsonResponse(context)


class AddArticleToShortcutView(View):
    @login_required
    def get(self, *args, **kwargs):
        context = {}
        article_id = self.request.GET.get('article_id')
        shortcut_id = self.request.GET.get('shortcut_id')

        article = Article.objects.get(pk=article_id)
        category = Category.objects.get(pk=shortcut_id)

        if category.articles.add(article):
            context['success'] = True

        return JsonResponse(context)


class ShowArticleFromShortcutView(View):
    @login_required
    def get(self, *args, **kwargs):
        context = {}
        shortcut_id = self.request.GET.get('shortcut_id')
        category = Category.objects.get(pk=shortcut_id)

        for article in Category.articles.exclude(status='w').exclude(status='d'):
            context.update({article.id: {
                'title': article.title,
                'author': article.author,
                'desc': article.description,
                'pub_date': article.publish_date.strftime("%d %B %Y %H:%M"),
                'useful': article.useful_counter,
                'viewed': article.view_counter,
                'loved': article.favorite_counter
            }})

        return JsonResponse(context)


class SetUsefulDailyRecapView(View):
    def get(self, *args, **kwargs):
        context = {}

        # daily_recap_id = self.request.GET.get('id')
        # action = self.request.GET.get('action')
        # q = DailyRecap.objects.get(id=daily_recap_id)
        # user = self.request.user
        #
        # try:
        #     p = UserDailyRecap.objects.all().get(user_id=user.id, daily_recap_id=daily_recap_id)
        #
        #     if action == 'true':
        #         p.useful = True
        #         q.useful_counter += 1
        #     else:
        #         p.useful = False
        #         q.useful_counter -= 1
        #
        #     p.save()
        #
        # except ObjectDoesNotExist:
        #     if action == 'true':
        #         UserDailyRecap.objects.create(user_id=user.id, daily_recap_id=daily_recap_id, useful=True)
        #         q.useful_counter += 1
        #
        # context.update({'useful_counter': q.useful_counter})
        # q.save()

        return JsonResponse(context)


class SetReadDailyRecapView(View):
    def get(self, *args, **kwargs):
        context = {}

        daily_recap_id = self.request.GET.get('id')
        q = DailyRecap.objects.get(id=daily_recap_id)
        user = self.request.user
        q.view_counter += 1
        q.save()

        return JsonResponse(context)


class ShowDailyRecapView(View):
    def get(self, *args, **kwargs):
        context = {}
        daily_recap_id = self.request.GET.get('id')
        user = self.request.user
        daily_recap = DailyRecap.objects.get(id=daily_recap_id)

        # try:
        #     UserDailyRecap.objects.get(user_id=user.id, daily_recap_id=daily_recap.pk, readed=True)
        #     readed = "ok"
        # except ObjectDoesNotExist:
        #     readed = "ko"
        #
        # try:
        #
        #     UserDailyRecap.objects.get(user_id=user.id, daily_recap_id=daily_recap.pk, useful=True)
        #     bigup = "ok"
        # except ObjectDoesNotExist:
        #     bigup = "ko"

        art = DailyRecap.objects.get(id=daily_recap.pk)

        attachments = ''
        for a in Attachment.objects.attachments_for_object(art):
            path, extension = os.path.splitext(a.attachment_file.name)
            extension = extension.replace(".", "")
            if extension in tf_ext:
                ext_class = 'tf'
            elif extension in df_ext:
                ext_class = 'df'
            elif extension in af_ext:
                ext_class = 'af'
            elif extension in vf_ext:
                ext_class = 'vf'
            elif extension in rif_ext:
                ext_class = 'rif'
            elif extension in plf_ext:
                ext_class = 'plf'
            elif extension in sf_ext:
                ext_class = 'sf'
            elif extension in cf_ext:
                ext_class = 'cf'
            else:
                ext_class = 'oth'
            filename = path.split("/")
            attachments += '<a class="attachment-file" href = "' + a.attachment_file.url + '" target="_blank">' \
                           + str(filename[len(filename) - 1]) + '<span class="ext_img ' + ext_class + '">' \
                           + extension.upper() + '</span></a>'

        context.update({'id': daily_recap.pk,
                        'title': daily_recap.title,
                        'desc': daily_recap.content,
                        'ok': 'ok',
                        'pub_date': daily_recap.publish_date.strftime("%d %B %Y"),
                        'views': daily_recap.view_counter,
                        'useful': daily_recap.useful_counter,
                        # 'read': readed,
                        # 'bigup': bigup,
                        'attachements': attachments,
                        })

        return JsonResponse(context)


class GetDailyRecapView(View):
    def get(self, user, **kwargs):

        context = {}
        from_date = self.request.GET.get('from_date')
        sorting = self.request.GET.get('sorting')
        nb = self.request.GET.get('nb')
        user = self.request.user
        groups = self.request.user.groups.values_list('name', flat=True)
        today = timezone.now()
        daily_recaps = DailyRecap.objects.all().filter(status='p').order_by('-publish_date')

        if sorting == 'today':
            daily_recaps.filter(publish_date__year=today.year, publish_date__month=today.month,
                                publish_date__day=today.day)
        elif sorting == 'past_7_days':
            daily_recaps.filter(publish_date__gte=timezone.now() - timedelta(days=7))
        elif sorting == 'this_month':
            daily_recaps.filter(publish_date__year=today.year, publish_date__month=today.month)
        elif sorting == 'this_year':
            daily_recaps.filter(publish_date__year=today.year)

        key = 0

        for daily_recap in daily_recaps[:int(nb)]:

            art = DailyRecap.objects.get(id=daily_recap.pk)

            # CHECK IF USER BELONG TO AUTHORIZED GROUP(S) OR AUTHORIZED USER(S)
            if art.is_public is False:
                if art.by_groups is True:
                    if len([i for i in groups if i in art.authorized_groups.values_list('name', flat=True)]) == 0:
                        continue
                elif art.by_groups is False:
                    if user.username not in art.authorized_users_dr.values_list('username', flat=True):
                        continue

            if art.publish_date.day == today.day:
                pub_date = 'Today'
            else:
                pub_date = art.publish_date.strftime("%d %B %Y")

            key += 1
            context.update({key: {
                'id': art.pk,
                'title': art.title,
                'pub_date': pub_date,
                'useful': art.useful_counter,
                'views': art.view_counter,
                'ok': 'ok',
                # 'bigup': bigup,
                # 'read': readed,
                'modified': art.modified.strftime("%d %B %Y"),
            }})

        return JsonResponse(context)


class GetArticlesByStaticShortcutsView(View):
    def get(self, user, **kwargs):

        # update_index.Command().handle()

        context = {}
        articles = []
        get_by = self.request.GET.get('by')
        display = self.request.GET.get('display')
        daily_recap = self.request.GET.get('is_daily')
        autocomplete = self.request.GET.get('autocomplete')
        autoquery = self.request.GET.get('autoquery')

        user = self.request.user
        groups = self.request.user.groups.values_list('name', flat=True)

        # AUTOCOMPLETE MODE
        if autocomplete == 'true':
            # sqs = SearchQuerySet().autocomplete(title_auto__startswith=autoquery)
            sqs = Article.objects.filter(title__icontains=autoquery)

            q = None
            for word in autoquery.split():
                q_aux = Q(title__icontains=word) | Q(content__icontains=word)
                q = (q_aux & q) if bool(q) else q_aux

            sqs = Article.objects.filter(q)

            if "#" in get_by:
                get_by = get_by.replace("#", "")
                tag = Tag.objects.get(name=get_by)
                for i in sqs:
                    for a in i.tags:
                        tmp = Tag.objects.get(pk=a)
                        if tmp.name == tag.name:
                            articles.append(i)
            else:
                articles = [result for result in sqs]

        # ARTICLE MODE
        else:

            if "#" not in get_by:
                try:
                    # p = SearchQuerySet().models(Article).exclude(status='d').exclude(status='w')
                    articles = Article.objects.filter(status='p')

                    if not Article.objects.all().filter(status='p') or not articles:
                        raise ObjectDoesNotExist
                    q = articles[0]
                except IndexError:
                    context.update({'msg': '<p style="padding: 16px;">No articles available, please add new ones '
                                           'or contact an administrator.</p>'})
                    return JsonResponse(context)
                except ObjectDoesNotExist:
                    context.update({'msg': '<p style="padding: 16px;">No articles available, please add new ones '
                                           'or contact an administrator.</p>'})
                    return JsonResponse(context)

                # GET HOME ARTICLES BY USEFUL COUNTER
                if get_by == 'Home':
                    articles = articles.order_by('-modified')
                # GET MOST USED ARTICLES
                elif get_by == 'Most Used':
                    articles = articles.order_by('-useful_counter')
                # GET MOST VIEWED ARTICLES
                elif get_by == 'Essential':
                    articles = articles.filter(essential=True)
                elif get_by == 'Most Viewed':
                    articles = articles.order_by('-view_counter')
                # GET MOST LOVED ARTICLES
                elif get_by == 'Most Loved':
                    articles = articles.order_by('-favorite_counter')
                # GET LAST UPDATES
                elif get_by == 'Last Updates':
                    for i in articles.order_by('-modified'):
                        x = Article.objects.get(pk=i.__getattribute__('pk'))
                        if x.modified != x.publish_date:
                            x.publish_date = x.modified
                            articles.append(x)
                # GET RECENT ARICLES
                elif get_by == 'Recent':
                    articles = articles.order_by('-publish_date')
                elif get_by == 'Historic':
                    try:
                        ids = user.get_related_articles_viewed()
                        for i in ids:
                            articles.append(Article.objects.get(id=i, status='p'))
                    except ObjectDoesNotExist:
                        context.update({'msg': 'Nothing for the moment :( Visit an article !'})
                        return JsonResponse(context)
                    except IndexError:
                        context.update({'msg': 'Nothing for the moment :( Visit an article !'})
                        return JsonResponse(context)
                # GET ARTICLES BY Categories OR TAGS
                elif get_by != 'Favorites' and get_by is not None:
                    # BY Categories
                    try:
                        p = Category.objects.get(name=get_by)
                        articles = p.articles.all()
                    except ObjectDoesNotExist:
                        context.update({'msg': 'No articles :( You can add new '
                                               'ones in <strong>' + get_by + '</strong> from admin interface !'})
                        return JsonResponse(context)
                    except IndexError:
                        context.update({'msg': 'No articles :( You can add new '
                                               'ones in <strong>' + get_by + '</strong> from admin interface !'})
                        return JsonResponse(context)
            # BY TAGS
            else:
                try:
                    get_by = get_by.replace("#", "")
                    tag = Tag.objects.get(name=get_by)
                    p = Article.objects.all()
                    for i in p:
                        for a in i.tags.all():
                            if a.name == tag.name:
                                articles.append(i)
                    if articles is None:
                        raise ObjectDoesNotExist
                except ObjectDoesNotExist:
                    context.update({'msg': 'There isn\'t articles with the tag'
                                           ' <strong>' + get_by + '</strong> for the moment :('})
                    return JsonResponse(context)
                except IndexError:
                    context.update({'msg': 'There isn\'t articles with the tag'
                                           ' <strong>' + get_by + '</strong> for the moment :('})
                    return JsonResponse(context)

        key = 0

        for article in articles:

            # IF FAVORITES CHECK IF USER LIKE THIS
            if get_by == 'Favorites':
                if user.username not in article.users_likes.values_list('username', flat=True):
                    break

            # CHECK IF USER BELONG TO AUTHORIZED GROUP(S) OR AUTHORIZED USER(S)
            if article.is_public is False:
                if article.by_groups is True:
                    if len([i for i in groups if i in article.authorized_groups.values_list('name', flat=True)]) == 0:
                        continue
                elif article.by_groups is False:
                    if user.username not in article.authorized_users.values_list('username', flat=True):
                        continue

            if user.username in article.users_likes.values_list('username', flat=True):
                favorites = "ok"
            else:
                favorites = "ko"

            if user.username in article.users_read.values_list('username', flat=True):
                read = "ok"
            else:
                read = "ko"

            if user.username in article.users_bigup.values_list('username', flat=True):
                bigup = "ok"
            else:
                bigup = "ko"

            tags = ''

            bookmarkclass = 'bookmarkLink'

            if article.url_content_option is True:
                url_option = 'ok'
                url = article.url_article
            else:
                url_option = 'ko'
                url = ''

            for a in article.tags.all()[:4]:
                tags += '<span class="badge bookmarkBadge"><span class="add-tags" style="display:none">' \
                        '<i class="material-icons">add_circle</i>' \
                        '</span><a id="#' + a.name + '" class="' + bookmarkclass + '" href="#">' + a.name + \
                        '</a></span>'

            attachments = ''
            nb_attachment = 0
            for a in Attachment.objects.attachments_for_object(article):
                nb_attachment += 1
                filename = a.attachment_file.name.split("/")
                attachments += '<a class="attachment-file" href = "' + a.attachment_file.url + '" target="_blank">' \
                               + str(filename[len(filename) - 1]) + '</a>'

            if get_by == 'Last Updates' and display != 'list':
                time = article.modified.strftime("%d %B %Y %H:%M")
                update = 'ok'
            else:
                time = article.publish_date.strftime("%d %b %Y")
                update = 'ko'

            if article.publish_date.day == timezone.now().day:
                newart = True
            else:
                newart = False

            key += 1
            context.update({key: {
                'id': article.pk,
                'title': article.title,
                'pub_date': time,
                'useful': article.useful_counter,
                'views': article.view_counter,
                'loved': article.favorite_counter,
                'favorites': favorites,
                'read': read,
                'url_option': url_option,
                'url': url,
                'attachments': attachments,
                'nb_attachment': nb_attachment,
                'newart': newart,
                'essential': article.essential,
                'bigup': bigup,
                # 'author': str(art.author),
                # 'tags': tags,
                # 'last_update': update,
                # 'modified': art.modified.strftime("%d %B %Y %H:%M"),
            }})

        return JsonResponse(context)


class SortArticlesView(View):
    @login_required
    def get(self, *args, **kwargs):
        context = {}

        # LOGIC HERE

        return JsonResponse(context)


class ShowArticleView(View):
    def get(self, *args, **kwargs):
        context = {}
        article_id = self.request.GET.get('id')
        user = self.request.user
        article = Article.objects.get(id=article_id)

        if user.username in article.users_likes.values_list('username', flat=True):
            favorites = "ok"
        else:
            favorites = "ko"

        if user.username in article.users_read.values_list('username', flat=True):
            read = "ok"
        else:
            read = "ko"

        if user.username in article.users_bigup.values_list('username', flat=True):
            bigup = "ok"
        else:
            bigup = "ko"

        tags = ''

        bookmarkclass = 'bookmarkLink'

        art = Article.objects.get(id=article.pk)

        if art.file_content_option is True:
            file_option = 'ok'
            file_url = art.file_content.url
        else:
            file_option = 'ko'
            file_url = ''

        for a in art.tags.all()[:7]:
            tags += '<span class="badge bookmarkBadge"><span class="add-tags" style="display:none">' \
                    '<i class="material-icons">add_circle</i>' \
                    '</span><a id="#' + a.name + '" class="' + bookmarkclass + '" href="#">' + a.name + \
                    '</a></span>'

        attachments = ''
        nb_attachment = 0
        for a in Attachment.objects.attachments_for_object(art):
            # if extension in tf_ext:
            #     ext_class = 'tf'
            # elif extension in df_ext:
            #     ext_class = 'df'
            # elif extension in af_ext:
            #     ext_class = 'af'
            # elif extension in vf_ext:
            #     ext_class = 'vf'
            # elif extension in rif_ext:
            #     ext_class = 'rif'
            # elif extension in plf_ext:
            #     ext_class = 'plf'
            # elif extension in sf_ext:
            #     ext_class = 'sf'
            # elif extension in cf_ext:
            #     ext_class = 'cf'
            # else:
            #     ext_class = 'oth'
            nb_attachment += 1
            filename = a.attachment_file.name.split("/")
            attachments += '<a class="attachment-file" href = "' + a.attachment_file.url + '" target="_blank">' \
                           + str(filename[len(filename) - 1]) + '</a>'

        if article.file_content_option is True:
            content = article.file_content.url
        else:
            content = article.content

        if article.title == '':
            title = article.file_content.name
        else:
            title = article.title

        context.update({'id': article.pk,
                        'title': title,
                        'author': str(article.author),
                        'desc': content,
                        'ok': 'ok',
                        'pub_date': article.publish_date.strftime("%d %B %Y"),
                        'views': article.view_counter,
                        'useful': article.useful_counter,
                        'loved': article.favorite_counter,
                        'tags': tags,
                        'favorites': favorites,
                        'read': read,
                        'bigup': bigup,
                        'attachements': attachments,
                        'file_option': file_option,
                        'file_url': file_url,
                        'nb_attachment': nb_attachment
                        })

        return JsonResponse(context)


class GetSortingMethodsView(View):
    def get(self, *args, **kwargs):
        context = {}

        return JsonResponse(context)


class GetFeedback(View):
    def get(self, *args, **kwargs):
        context = {}
        feedback_choice = self.request.GET.get('feedback_choice')
        feedback_text = self.request.GET.get('feedback_text')
        article_id = self.request.GET.get('id')
        user = self.request.user

        obj = Feedback.objects.create(date=timezone.now(), author=user, rate=feedback_choice,
                                      explanation=feedback_text, article=Article.objects.get(id=article_id))

        obj.save()

        return JsonResponse(context)


class GetPollsView(View):
    def get(self, *args, **kwargs):
        context = {}
        polls = []
        questions = {}
        poll_id = self.request.GET.get('id')
        sorting = self.request.GET.get('sorting')
        nb = self.request.GET.get('nb')
        if nb is None:
            nb = 100
        user = self.request.user
        groups = self.request.user.groups.values_list('name', flat=True)
        today = timezone.now()
        choices = {}

        if poll_id != '':
            poll = Poll.objects.get(id=poll_id)

            for question in poll.questions.all():
                if question.illustration:
                    file = question.illustration.url
                else:
                    file = ''
                questions.update({question.title: {}})
                for choice in question.choices.all():
                    questions[question.title].update(
                        {choice.id: {'choice_id': choice.id, 'choice_title': choice.title, 'type': choice.type,
                                     'img_url': file}})

            context.update({poll.id: {
                'poll_title': poll.title,
                'questions': questions,
                'pub_date': poll.publish_date.strftime("%d %B %Y")
            }})
        elif sorting == 'today':
            polls = Poll.objects.all().filter(publish_date__year=today.year, publish_date__month=today.month,
                                              publish_date__day=today.day).order_by('-publish_date')
        elif sorting == 'past_7_days':
            polls = Poll.objects.all().filter(publish_date__gte=timezone.now() - timedelta(days=7)) \
                .order_by('-publish_date')
        elif sorting == 'this_month':
            polls = Poll.objects.all().filter(publish_date__year=today.year, publish_date__month=today.month) \
                .order_by('-publish_date')
        elif sorting == 'this_year':
            polls = Poll.objects.all().filter(publish_date__year=today.year).order_by('-publish_date')
        else:
            polls = Poll.objects.all().order_by('-publish_date')

        for poll in polls[:int(nb)]:
            nb_question = 0
            for question in poll.questions.all():
                nb_question += 1
                questions.update({question.title: {}})
                for choice in question.choices.all():
                    questions[question.title].update({choice.id: {'choice_id': choice.id, 'choice_title': choice.title,
                                                                  'type': choice.type}})

            context.update({poll.id: {
                'poll_title': poll.title,
                'questions': questions,
                'pub_date': poll.publish_date.strftime("%d %B %Y"),
                'nb_question': nb_question,
                'current_question': poll.id_current_question

            }})

        return JsonResponse(context)


class WrongOrRightView(View):
    def get(self, *args, **kwargs):
        context = {}
        choice_id = self.request.GET.get('choice_id')

        if (Choice.objects.get(id=choice_id)).type == '0':
            context.update({'ok': 'ok'})

        return JsonResponse(context)


class GetAttachmentsView(View):
    def get(self, *args, **kwargs):
        context = {}
        id = self.request.GET.get('id')
        art = Article.objects.get(id=id)
        attachments = ''
        nb_attachment = 0
        for a in Attachment.objects.attachments_for_object(art):
            nb_attachment += 1
            filename = a.attachment_file.name.split("/")
            attachments += '<a class="attachment-file" href = "' + a.attachment_file.url + '" target="_blank">' \
                           + str(filename[len(filename) - 1]) + '</a>'

        context.update({'attachments': attachments})

        return JsonResponse(context)


class GetMostPopularTags(View):
    def get(self, *args, **kwargs):
        context = {}
        popular_tags = []

        popular_articles = Article.objects.all().order_by('view_counter')[:10]

        for articles in popular_articles:
            for tag in articles.tags.all().order_by('click_counter')[:20]:
                context.update({tag.name: tag.name})

        return JsonResponse(context)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.db.utils import DatabaseError
from django.views.generic import FormView
from .forms import GenerateUsersForm
from .models import KnowledgeBase
from random import choice
from django.views.generic import View
from django.http import JsonResponse

from apps.article.models import Category


@login_required
def index(request):
    return render(request, 'core/home.html', {'nodes_static': Category.objects.all().filter(static=True),
                                              'nodes_variable': Category.objects.all().filter(static=False)},
                  context_instance=RequestContext(request))


def poll(request):
    return render(request, 'core/data.html')


def daily_recap(request):
    return render(request, 'core/daily_recap.html', {'nodes_static': Category.objects.all().filter(static=True),
                                                     'nodes_variable': Category.objects.all().filter(static=False)},
                  context_instance=RequestContext(request))


class TenantView(FormView):
    form_class = GenerateUsersForm
    template_name = "index_tenant.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(TenantView, self).get_context_data(**kwargs)
        context['tenants_list'] = KnowledgeBase.objects.all()
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form):
        User.objects.all().delete()  # clean current users

        # generate five random users
        USERS_TO_GENERATE = 5
        first_names = ["Aiden", "Jackson", "Ethan", "Liam", "Mason", "Noah",
                       "Lucas", "Jacob", "Jayden", "Jack", "Sophia", "Emma",
                       "Olivia", "Isabella", "Ava", "Lily", "Zoe", "Chloe",
                       "Mia", "Madison"]
        last_names = ["Smith", "Brown", "Lee	", "Wilson", "Martin", "Patel",
                      "Taylor", "Wong", "Campbell", "Williams"]

        while User.objects.count() != USERS_TO_GENERATE:
            first_name = choice(first_names)
            last_name = choice(last_names)
            try:
                user = User(username=(first_name + last_name).lower(),
                            email="%s@%s.com" % (first_name, last_name),
                            first_name=first_name,
                            last_name=last_name)
                user.save()
            except DatabaseError:
                pass

        return super(TenantView, self).form_valid(form)


class CreateTenantView(FormView):
    form_class = GenerateUsersForm
    template_name = "index_tenant.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super(CreateTenantView, self).get_context_data(**kwargs)
        context['tenants_list'] = KnowledgeBase.objects.all()
        context['users'] = User.objects.all()
        return context

    def form_valid(self, form):
        User.objects.all().delete()  # clean current users

        # generate five random users
        USERS_TO_GENERATE = 5
        first_names = ["Aiden", "Jackson", "Ethan", "Liam", "Mason", "Noah",
                       "Lucas", "Jacob", "Jayden", "Jack", "Sophia", "Emma",
                       "Olivia", "Isabella", "Ava", "Lily", "Zoe", "Chloe",
                       "Mia", "Madison"]
        last_names = ["Smith", "Brown", "Lee	", "Wilson", "Martin", "Patel",
                      "Taylor", "Wong", "Campbell", "Williams"]

        while User.objects.count() != USERS_TO_GENERATE:
            first_name = choice(first_names)
            last_name = choice(last_names)
            try:
                user = User(username=(first_name + last_name).lower(),
                            email="%s@%s.com" % (first_name, last_name),
                            first_name=first_name,
                            last_name=last_name)
                user.save()
            except DatabaseError:
                pass

        return super(CreateTenantView, self).form_valid(form)


class GetTenantStyle(View):
    def get(self, *args, **kwargs):
        context = {}

        pr_color = self.request.tenant.primary_color
        sc_color = self.request.tenant.secondary_color

        context.update({'primary_color': pr_color, 'secondary_color': sc_color, 'img': 'img'})

        return JsonResponse(context)



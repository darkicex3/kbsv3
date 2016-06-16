from apps.core.models import KnowledgeBase
from django.conf import settings
from django.db import utils
from django.views.generic import TemplateView
from tenant_schemas.utils import remove_www
from django.contrib.auth.decorators import login_required


class HomeView(TemplateView):
    template_name = "index_public.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        hostname_without_port = remove_www(self.request.get_host().split(':')[0])

        try:
            KnowledgeBase.objects.get(schema_name='public')
        except utils.DatabaseError:
            context['need_sync'] = True
            context['shared_apps'] = settings.SHARED_APPS
            context['tenants_list'] = []
            return context
        except KnowledgeBase.DoesNotExist:
            context['no_public_tenant'] = True
            context['hostname'] = hostname_without_port

        if KnowledgeBase.objects.count() == 1:
            context['only_public_tenant'] = True

        context['tenants_list'] = KnowledgeBase.objects.all()
        return context

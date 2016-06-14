from django.http import JsonResponse
from django.views.generic import View

from apps.article.models import Category


class ManageSidebarShortcutsShowingView(View):
    def get(self, *args, **kwargs):
        context = {}
        is_child = False

        try:
            categories = Category.objects.all().filter(activated=True)
            q = categories[0]
        except IndexError:
            context.update({'msg': '<p style="padding: 16px;">No shortcuts available, please add new ones '
                                   'or contact an administrator.</p>'})
            return JsonResponse(context)

        for category in categories:
            children = {}
            has_children = False
            for child in category.get_children():
                children.update({child.id: {'child_name': child.name}})
                has_children = True

            print('CATEGORIES', category.name, children, has_children)
            context.update({category.id: {
                'name': category.name,
                'static': category.static,
                'icon': category.icon,
                'children': children,
                'has_children': has_children
            }})

        return JsonResponse(context)


class ManageSidebarShortcutsEditingView(View):
    def post(self, *args, **kwargs):

        context = {'success': True}

        for key, value in self.request.POST.items():
            category = Category.objects.get(key)
            category.activated = value

        return JsonResponse(context)


class ManageSidebarShortcutsInsertingView(View):
    def post(self, *args, **kwargs):

        context = {}
        shortcut_name = self.request.POST('shortcut_name')
        q = Category.objects.create(shortcut_name=shortcut_name)

        if q:
            context.update({q.id: {'success': True}})

        return JsonResponse(context)












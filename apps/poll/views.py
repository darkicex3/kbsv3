from django.http import JsonResponse
from django.views.generic import View
from apps.poll.models import Poll, Choice


class GetCurrentQuestionView(View):
    def get(self, *args, **kwargs):
        context = {}
        poll_id = self.request.GET.get('id')
        mode = self.request.GET.get('mode')
        current_id = self.request.GET.get('current_id')
        poll = Poll.objects.get(id=poll_id)

        if mode == 'w':
            poll.id_current_question = int(current_id)
            poll.save()
            context.update({'ok': 'ok'})
        else:
            context.update({'current_question': poll.id_current_question})

        return JsonResponse(context)

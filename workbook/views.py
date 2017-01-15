from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone
from .models import Choice, Question

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'workbook/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published
        # questions (not including those set to be published in the future).
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'workbook/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'workbook/results.html'


def vote(request, question_id):
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    # Redisplay the question voting form.
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'workbook/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('workbook:results', args=(p.id,)))

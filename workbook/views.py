from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.TemplateView):
    template_name = 'workbook/index_page.html'

    def get(self, request, *args, **kwargs):
        test_list = ['SAMPLE_ONE', 'SAMPLE_TWO']
        return render(request, self.template_name, {'test_list': test_list})


class ProjectsView(generic.TemplateView):
    template_name = 'workbook/projects_page.html'


class ContactView(generic.TemplateView):
    template_name = 'workbook/contact_page.html'


class AboutView(generic.TemplateView):
    template_name = 'workbook/about_page.html'



## --------------------------------------------------
## Below located work part as Sample
## TODO (Stubs) Remove Helper Stubs


class IndexView1(generic.ListView):
    template_name = 'workbook/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        # Return the last five published questions
        # (not including those set to be published in the future).
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

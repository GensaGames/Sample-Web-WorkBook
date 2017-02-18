import os

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.views import generic

from webworkbook import settings
from .models import Choice, Question


class IndexView(generic.TemplateView):
    template_name = 'workbook/index_page.html'


    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'stories_list': self.generate_stories()})


    def generate_stories(self):
        stories_main_dir = os.path.join(settings.STATICFILES_DIRS[0], 'workbook', 'stories')
        stories_list = list()
        # Iterate all static folder for Articles and Stories
        # USE UNICODE METHOD, which missing on Python >= 3.5
        for parent_file in os.listdir(stories_main_dir):
            story_dir = os.path.join(stories_main_dir, parent_file)
            story_img_source = story_text_source = story_header = None
            if not os.path.isdir(story_dir):
                continue
            # Gather all items, from Stories, like Tittle, Text and Img.
            for story_file in os.listdir(story_dir):
                story_iter_type = os.path.splitext(story_file)
                if story_iter_type[1] == '.png' or story_iter_type[1] == '.jpg':
                    story_img_source = os.path.join(story_dir, story_file)
                    story_img_source = story_img_source.replace(settings.BASE_DIR, '')
                if story_iter_type[1] == '.txt':
                    with open(os.path.join(story_dir, story_file), 'r') as story:
                        story_text_source = unicode(story.read(), errors='ignore')
                        story_header = story_iter_type[0]
            # Using list of tuples this items and transfer.
            if story_header is not None and story_text_source is not None \
                    and story_img_source is not None:
                stories_list.append((story_header, story_text_source, story_img_source))
        return stories_list


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

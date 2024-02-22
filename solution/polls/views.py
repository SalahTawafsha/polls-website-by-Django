""" views of my polls project. """

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .forms import QuestionForm
from .models import Choice, Question


class IndexView(generic.ListView):
    """ Index view of polls app. """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")


class DetailView(generic.DetailView):
    """ Detail view of polls app. """
    model = Question
    template_name = "polls/question_detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    """ Results view of polls app. """
    model = Question
    template_name = "polls/results_detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    """ Vote script of polls app and return results if success. """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(
            request,
            "polls/question_detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    selected_choice.votes += 1
    selected_choice.save()
    # Always return an HttpResponseRedirect after successfully dealing
    # with POST data. This prevents data from being posted twice if a
    # user hits the Back button.
    return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


def create_question(request):
    """ View for creating a new question. """
    if request.method == "POST":

        form = QuestionForm(request.POST)
        if form.is_valid():
            question = Question(question_text=form.cleaned_data["question_text"], pub_date=timezone.now())
            question.save()
            options = request.POST.getlist("options[]")

            is_there_option = False
            for option in options:
                if option != "":
                    question.choice_set.create(choice_text=option, votes=0)
                    is_there_option = True

            if not is_there_option:
                question.delete()
                return render(request, "polls/create.html", {"form": form, "error_message": "You didn't add any option."})
            return HttpResponseRedirect(reverse("polls:index"))
    else:
        form = QuestionForm()
    return render(request, "polls/create.html", {"form": form})

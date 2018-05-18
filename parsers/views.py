from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic.base import View
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from parsers.main import main
from parsers.parser_engine.set_timestamp import set_timestamp
from parsers.models import UserQuery, Document, BaseUrlParser, Tags
from parsers.forms import NewQueryFrom


class Dash(ListView):
    model = UserQuery
    template_name = 'parsers/dash.html'


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/login/"
    template_name = "parsers/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "parsers/login.html"
    success_url = "/"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect("/")


class QueryListView(ListView):
    model = UserQuery
    context_object_name = 'userquerys'
    paginate_by = 4


class SearchView(QueryListView):
    def get(self, request, *args, **kwargs):
        tag_name = request.GET.get('tag')
        tag = get_object_or_404(Tags, name_tag=tag_name)
        queries = tag.userquery_set.all()
        context = {
            'userquerys': queries,
        }
        return render_to_response(template_name='parsers/userquery_list.html', context=context)


def new_query(request):
    if request.method == 'POST':
        form = NewQueryFrom(request.POST)
        if form.is_valid():
            set_timestamp()
            result = main(**form.cleaned_data)
            query = UserQuery(**result['UserQuery'])
            query.user_id = request.user.id
            query.save()
            for tag_name in list(result['UserQuery'].values())[1:]:
                if tag_name:
                    tag, _ = Tags.objects.get_or_create(name_tag=tag_name)
                    query.tags.add(tag)
            for doc in result['Document']:
                doc['user_query_id'] = int(query.id)
                document = Document(**doc)
                document.save()
            result['BaseUrlParser']['user_query_id'] = int(query.id)
            baseurl = BaseUrlParser(**result['BaseUrlParser'])
            baseurl.save()
            url = query.get_url()
            data = {
                'url': url,
                'message': 'ok'
            }
            return JsonResponse(data)
        data = {
            'url': '/',
            'message': 'form is not validate'
        }
        return JsonResponse(data)
    else:
        form = NewQueryFrom()
    return render(request, 'parsers/new_query.html', {
        'form': form
    })


class UserQueryDetail(DetailView):
    model = UserQuery
    slug_field = 'timestamp'

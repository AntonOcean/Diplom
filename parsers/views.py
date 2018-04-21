from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.http import request, JsonResponse, Http404
from django.views.decorators.http import require_POST
from parsers.models import UserQuery, Document, BaseUrlParser
from parsers.forms import NewQueryFrom
from time import sleep
from parsers.forms import NewQueryFrom
from django.views.generic import ListView, FormView
from django.views.generic import DetailView
from parsers.main import main
from parsers.parser_engine.set_timestamp import set_timestamp
#from rest_framework.pagination import CursorPagination


class QueryListView(ListView):
    model = UserQuery
    context_object_name = 'userquerys'
    paginate_by = 5


def new_query(request):
    if request.method == 'POST':
        form = NewQueryFrom(request.POST)
        if form.is_valid():
            set_timestamp()
            result = main(**form.cleaned_data)
            query = UserQuery(**result['UserQuery'])
            query.save()
            print(result)
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
            return HttpResponseRedirect('/')
            #return JsonResponse(data)
        data = {
            'url': '/',
            'message': 'form is not validate'
        }# отдаем в феил
        return JsonResponse(data)
    else:
        form = NewQueryFrom()
    return render(request, 'parsers/new_query.html', {
        'form': form
    })

# def queries_list(request):
#     userquery_list = UserQuery.objects.all()
#     paginator = Paginator(userquery_list, 5) # Show 25 contacts per page
#     page = request.GET.get('page')
#     userquerys = paginator.get_page(page)
#     return render(request, 'parsers/queries_list.html', {'userquerys': userquerys})


# def test(request):
#     return render(request, 'parsers/ex.html')
#
# def test_ajax(request):
#     print('Hello', request)
#     return render(request, "parsers/ajax_info.html", {})



def login(request):
    pass

def signup(request):
    pass

# def load(request):
#     return render(request, 'parsers/load.html')
#
#
# def query_detail(request, slug):
#     query = get_object_or_404(UserQuery, slug=slug)
#     return render(request, 'parsers/query_detail.html', {
#         'query': query,
#         'base_urls': query.baseurlparser_set.all().first(),
#         'documents': query.document_set.all()
#     })

class UserQueryDetail(DetailView):
    model = UserQuery
    slug_field = 'timestamp'



from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib2
import HTML
import db
from .forms import UrlForm

@csrf_exempt
def search_kb(request,id):
    results = db.search_file_name(id)
    colored_state = lambda state : HTML.TableCell(state, bgcolor='lime' if state == 'ProcessCompleted' else 'red')
    table_data = [[row[0], row[1], colored_state(row[2]), HTML.link(row[7],'search_extracted/'+str(row[0])+'/'), row[3], HTML.link('Download', row[4]), \
                 HTML.link('Open', 'file:///' + row[5].replace('\\','/')), "{:%d/%m/%y}".format(row[6])] for row in results]
    htmlcode = HTML.table(table_data, header_row=['Id','File Name','State','#Extracted','Status','Url','Local Path','Retrieval Date'])	
    return HttpResponse(htmlcode)

@csrf_exempt
def search_extracted(request,id):
    results = db.search_extracted(id)
    table_data = [row[0] for row in results]
    return HttpResponse('<br/>'.join(table_data))
	
@csrf_exempt
def get_page(request):
    form = UrlForm(request.POST)
    if not form.is_valid():
        raise Exception("invalid form")
    url = form.cleaned_data['url']
    response = urllib2.urlopen(url)
    content = response.read()
    source_content_type = response.info().get('content-type')
    return HttpResponse(content, content_type=source_content_type)



from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib2
import HTML
import db
from .forms import UrlForm
import re
import datetime

@csrf_exempt
def search_kb(request,id):
    results = db.search_file_name(id) #[[123,'sdfsdhdff','ProcessCompleted','setet','http://www.google.com','c:\\\\',datetime.datetime.now(),4]]
    if len(results) == 0:
        htmlcode = HTML.table([[HTML.TableCell('Not Found', bgcolor='red')]])
        return HttpResponse(htmlcode)
    colored_state = lambda state : '<span style="background-color: %s">%s</span>' % ('lime' if state == 'ProcessCompleted' else 'red', state)
    table_data = [[row[0], row[1], colored_state(row[2]), HTML.link(row[7],'search_extracted/'+str(row[0])+'/'), row[3], HTML.link('Download', row[4]), \
                 HTML.link('Open', 'file:///' + row[5].replace('\\','/')), "{:%d/%m/%y}".format(row[6])] for row in results]
    htmlcode = HTML.table(table_data, header_row=['Id','File Name','State','#Extracted','Status','Url','Local Path','Retrieval Date'])	
    return HttpResponse(htmlcode)

@csrf_exempt
def search_extracted(request,id):
    results = db.search_extracted(id)
    table_data = [row[0] for row in results]
    return HttpResponse('<br/>'.join(table_data))

#TODO: search files including extracted
#TODO: multiple search (find pattern in text area)

@csrf_exempt
def get_page(request):
    form = UrlForm(request.POST)
    if not form.is_valid():
        raise Exception("invalid form")
    url = form.cleaned_data['url']
    response = urllib2.urlopen(url)
    content = response.read()
    source_content_type = response.info().get('content-type')
    content = re.sub(r"\b(\d{7})\b",r"<b>\1</b>",content) #find numbers to mark
    return HttpResponse(content, content_type=source_content_type)



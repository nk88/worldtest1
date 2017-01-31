from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib2
import HTML
import db

@csrf_exempt
def search_kb(request,id):
    results = db.search_file_name(id)
    colored_state = lambda state : HTML.TableCell(state, bgcolor='lime' if state == 'ProcessCompleted' else 'red')
    table_data = [[row[0], row[1], colored_state(row[2]), row[3], HTML.link('Download', row[4]), \
                 HTML.link('Open', 'file:///' + row[5].replace('\\','/')), "{:%B %d/%m/%y}".format(row[6])] for row in results]
    htmlcode = HTML.table(table_data, header_row=['Id','File Name','State','Status','Url','Local Path','Retrieval Date'])	
    """
    table_data = [
        #[id,       'success'],
        [id, HTML.TableCell('success', bgcolor='lime'), HTML.link('Download', 'http://www.google.com/'), HTML.link('Open dir', 'file:///C:/Windows/')],
    ]
    result_colors = {
        'success':      'lime',
        'failure':      'red',
        'error':        'yellow',
    }
    htmlcode = HTML.Table(header_row=['ID', 'Status'])
    for row in table_data:
        # create the colored cell:
        colored_result = HTML.TableCell(row[1], bgcolor=result_colors[row[1]])
        # append the row with two cells:
        htmlcode.rows.append([row[0], colored_result])	
    #return HttpResponse("stam " + id)
    """
    return HttpResponse(htmlcode)
	
@csrf_exempt
def get_page(request):
    url = request.body
    content = urllib2.urlopen(url).read()
    return HttpResponse(content)


from django.http import HttpResponse
from django.utils import simplejson

def login(request):

    if request.method == "POST":

        username = request.POST.get('username', None)
        password = request.POST.get('password', None)

        u = 'dave'
        p = 'shart'

        if username == u and password == p:
            data = {'result': "success"
                    }
            status_code = 200
        else:
            data = {'result': "failure"
                    }
            status_code = 404

        json_data = simplejson.dumps(data)
        return HttpResponse(json_data,
                            mimetype='application/json; charset=utf-8',
                            status=status_code
                            )
from django.http import HttpResponse
from django.template import loader
import gapi
# Create your views here.


def product_qr(request):
    template = loader.get_template('qr_template.html')
    qr_id = request.path.split('/')[-1]
    qr_detail = gapi.qr_detail(qr_id)
    context = {"name":qr_detail[0]['value'],"qr_detail":qr_detail[1:]}
    print(context)
    return HttpResponse(template.render(context,request))

from django.http import HttpResponse
from django.template import loader

# Create your views here.


def product_qr(request):
    template = loader.get_template('qr_template.html')
    qr_id = request.path.split('/')[-1]
    return HttpResponse(template.render())

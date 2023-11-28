from django.http import HttpResponse
from django.template import loader
import gapi
from .models import QR
import dapi
# Create your views here.


def product_qr(request):
    template = loader.get_template('qr_template.html')
    qr_id = request.path.split('/')[-1]
    qr_detail = dapi.qr_detail(qr_id)
    context = {"name":qr_detail[0]['value'],"qr_detail":qr_detail[1:]}
    return HttpResponse(template.render(context,request))

def qr_list(request):
    template = loader.get_template('all_qr.html')
    qr_id = request.path.split('/')[-1]
    qr_one = dapi.qr_detail(qr_id)
    context = {'qrs':qr_one}
    return HttpResponse(template.render(context,request))

def migrate(requests):
    sheetnames = gapi.sheet_names()
    tb_name = [['qtype','name']]
    for i in range(len(sheetnames)):
        tb_name.append([sheetnames[i],"type_"+str(i)])
        if i>1: #bỏ qua sheet đầu
            sheetvalues = gapi.sheet_values(sheetnames[i])
            dapi.migrate_table(sheetvalues,"type_"+str(i))
    dapi.migrate_table(tb_name,"tb_name",True)
    sheetvalues = gapi.sheet_values('QR')
    sheetvalues.insert(0,['qrid','qtype','status'])
    dapi.migrate_table(sheetvalues, 'QR',True)
    return HttpResponse('migration done')
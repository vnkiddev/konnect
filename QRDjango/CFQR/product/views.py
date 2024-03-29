from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import render, redirect
import gapi,os

import dapi
# Create your views here.


def product_qr(request):
    template = loader.get_template('qr_template.html')
    qr_id = request.path.split('/')[-1]
    qr_id = qr_id.split('?')[0]
    if qr_id == 'favicon.ico':
        return HttpResponseRedirect('/static/favicon.ico')
    elif qr_id == "":
        return redirect("http://connectfashion.com.vn")
    qr_detail = dapi.qr_detail(qr_id)
    img_list = [filename for filename in os.listdir('product/static') if (filename == qr_id+".jpg" or filename.startswith(qr_id+"-"))]
    common = ["/rami/"+filename for filename in os.listdir('product/static/rami')]
    img_list.extend(common)
    print(img_list)
    context = {"name":qr_detail[1]['value'],"qr_detail":qr_detail[2:], "fistimg":img_list[0],"imglist":img_list[1:]}
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


def product_image(request):
    template = loader.get_template('upload_img.html')
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save('product   b/static/'+ myfile.name, myfile)
        uploaded_file_url = 'static/'+myfile.name
        return HttpResponse(template.render({
            'uploaded_file_url': uploaded_file_url
        },request))
    return HttpResponse(template.render({},request))
from xml.dom.minidom import Document
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.storage import FileSystemStorage
from .forms import UploadFileForm
from django.conf import settings
from django.contrib import messages
import pandas as pd
import os
import json
from django.views.decorators.csrf import csrf_exempt
import csv

# Create your views here.
def home(request):
    return render(request, "home.html")

# # CSV file upload
# def csv_file(request):
#     if request.method == "POST":
#         file = request.body



@csrf_exempt
def csv_file_react(request):
    if request.method =="POST":
        uploadedfile = request.FILES['Document']
        fileName = uploadedfile.name
        fs = FileSystemStorage()    #Creating an object
        fs.save(fileName, uploadedfile)
        if fileName.endswith('.csv'):
            data = pd.read_csv(os.path.join(settings.MEDIA_ROOT,fileName))
        elif fileName.endswith('.xls'):
            data = pd.read_excel(os.path.join(settings.MEDIA_ROOT,fileName))   
        else:
            messages.warning(request,"Incorrect file format")
            return HttpResponse("Incorrect file format")
            # return redirect('Upload')
        html_data = data.to_json()
        # return render(request,'visualize.html',{'data':html_data})
        return HttpResponse(html_data)

    # GET
    else:
        # return render(request, "upload.html")
        return HttpResponse("GET")

@csrf_exempt
def csv_file(request):
    if request.method =="POST":
        body= request.body.decode('utf-8')
        body = json.loads(body)
        uploadedfile =body['formData']
        
        filename =  uploadedfile['file']
        data = uploadedfile['data']
     
        name = os.path.join(settings.MEDIA_ROOT,filename)

        with open(name , 'w', newline='') as file:
            writer = csv.writer(file)
            for d in data:
                writer.writerow(d)

        data = pd.read_csv(os.path.join(settings.MEDIA_ROOT,filename))
        html_data = data.to_html()
        html = html_data.lstrip('<table border="1" class="dataframe">').rstrip("</table>")
        send = {'html':html,  'name':filename}
        print(send)
        return JsonResponse(send)
            

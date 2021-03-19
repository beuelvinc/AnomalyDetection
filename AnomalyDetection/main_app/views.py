from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from .utils import *
import  traceback

def home(request):
    if request.method == 'POST':
        try:
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                file = request.FILES['file']
                data = file.read()
                file_handler = CsvFile(data)
                image = file_handler.pic_hash
                data = file_handler.all_data

                json_data=handle_json(data)
                return render(request, 'main.html', {'image': image,'json_data':json_data})
        except Exception as e:
            traceback.print_exc()
            return render(request, 'main.html', {'error': True})


    else:
        form = UploadFileForm()
    return render(request, 'main.html', {'form': form})

from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from leases.forms import UploadFileForm
from django.utils.encoding import smart_str
import os 
from leases.generator import Generator
import zipfile
import StringIO

upload_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'media')

newbatch = Generator()


def index(request):
    return render(request, 'leases/index.html')

def bulk(request):
    
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        dir_file = os.path.join(upload_path, filename)
        newbatch.importcsv(dir_file)
        newbatch.generateform()
        nbcf = newbatch.filenames
        outname = 'output/'
        filenames = [outname + x for x in nbcf]
        # Folder name in ZIP archive which contains the above files
        # E.g [thearchive.zip]/somefiles/file2.txt
        # FIXME: Set this to something better
        zip_subdir = "unsignedleases"
        zip_filename = "%s.zip" % zip_subdir

        # Open StringIO to grab in-memory ZIP contents
        s = StringIO.StringIO()

        # The zip compressor
        zf = zipfile.ZipFile(s, "w")

        for fpath in filenames:
            # Calculate path for file in zip
            fdir, fname = os.path.split(fpath)
            zip_path = os.path.join(zip_subdir, fname)

            # Add file, at correct path
            zf.write(fpath, zip_path)

        # Must close zip for all contents to be written
        zf.close()

        # Grab ZIP file from in-memory, make response with correct MIME-type
        resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
        # ..and correct content-disposition
        resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

        return resp

    else:
        return render(request, 'leases/bulk.html')

def approved(request):
    return render(request, 'leases/approved.html')

def upload(request):
    return render(request, 'leases/upload.html')
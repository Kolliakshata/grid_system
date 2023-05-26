import csv,json
from django.shortcuts import render,HttpResponse
from .models import Student
from django.db.models import Q
from .utils import CSVUploadForm 
from django.core.paginator import Paginator
from django.http import JsonResponse



def upload_csv(request):
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csvfile = request.FILES['csv_file']
            reader = csv.DictReader(csvfile.read().decode('utf-8-sig').splitlines())
            for row in reader:
                id = int(row['id'])
                name = row['name']
                total_marks = row['total_marks']
                # Create an instance of YourModel and save it to the database
                obj = Student(id=id, name=name, total_marks=total_marks)
                obj.save()

    else:
        form = CSVUploadForm()

    return render(request, 'student.html', {'form': form})




def load_student_details(request):
    page_number = request.GET.get('page_number', 5)
    page_size = request.GET.get('page_size', 10)

    students = Student.objects.all()
    
    paginator = Paginator(students, page_size)
    page = paginator.get_page(page_number)

    data = {
        'page_number': page.number,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_students': paginator.count,
        'students': list(page),
    }
    
    return render(request, 'result.html', data)


def filter_student_details(request):
    page_number = request.GET.get('page_number', 1)
    page_size = request.GET.get('page_size', 10)
    filter_criteria = request.GET.get('filter_criteria', 'Tore')

    students = Student.objects.filter(Q(name__icontains=filter_criteria) | Q(total_marks__icontains=filter_criteria))
    paginator = Paginator(students, page_size)
    page = paginator.get_page(page_number)

    data = {
        'page_number': page.number,
        'page_size': page_size,
        'total_pages': paginator.num_pages,
        'total_students': paginator.count,
        'students': list(page),
    }

    return render(request, 'result.html',data)
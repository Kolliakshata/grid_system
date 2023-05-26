from django.urls import path
from .views import upload_csv,load_student_details,filter_student_details

urlpatterns = [
    path('load_student_details/', load_student_details, name='load_student_details'),
    path('uploadfile/', upload_csv, name='upload_csv'),
    path('filer_student/', filter_student_details, name='filer name'),

]

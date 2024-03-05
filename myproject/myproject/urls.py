from django.contrib import admin
from django.urls import include, path
from students_management.views import StudentApi,StudentsByStandardApi,StandardApi
from students_management.views import StudentList,SearchFormView,index,insert

urlpatterns = [
    path('', index, name='index'),
    path('admin/', admin.site.urls),
    path('students/insert', insert, name='insert'),
    path('students/', StudentApi.as_view(), name='student-api'),
  path('search/', SearchFormView.as_view(), name='student-search'),
     path('students/<int:pk>/', StudentApi.as_view(), name='student-detail'),
     path('standards/', StandardApi.as_view(), name='standard-list'),
    path('standards/<int:standard_id>/', StandardApi.as_view(), name='standard-detail'),
      path('students/standard/<int:standard_id>/', StudentsByStandardApi.as_view(), name='students-by-standard'),  # New URL for students by standard
    # Include other URLs as needed
]
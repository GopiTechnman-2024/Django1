from django.http import JsonResponse
from django.shortcuts import redirect, render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Student
from .serializers import StandardSerializer, StudentSerializer
from .models import Standard
from rest_framework.pagination import PageNumberPagination
from django.core.paginator import Paginator,EmptyPage
from django.views.generic import TemplateView

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'  # User-defined page size parameter

class StudentList(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        students = Student.objects.all()
        paginator = CustomPagination()
        result_page = paginator.paginate_queryset(students, request)
        serializer = StudentSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

class CustomPagination(PageNumberPagination):
    page_size_query_param = 'page_size'


class StudentTableView(TemplateView):
    template_name = 'students_management/students.html'

    def get_context_data(self, **kwargs):
        search_query = self.request.GET.get('q', '')
        students = Student.objects.all()

        if search_query:
            students = students.filter(name__icontains=search_query)

        students = students.order_by('name')
        paginator = Paginator(students, 2)
        page_number = self.request.GET.get('page', 1)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)

        context = {
            'students': page,
            'search_query': search_query,
        }
        return context


class SearchFormView(TemplateView):
    template_name = 'students_management/search.html'


class PaginationView(TemplateView):
    template_name = 'students_management/pagination.html'


class StudentApi(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        search_query = request.GET.get('q', '')
        students = Student.objects.all()

        if search_query:
            students = students.filter(name__icontains=search_query)

        students = students.order_by('name')
        paginator = Paginator(students, 2)
        page_number = request.GET.get('page', 1)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(1)

        context = {
            'students': page,
            'search_query': search_query,
        }
        return render(request, 'students_management/students.html', context)
        # student_id = request.query_params.get('id')
        # if student_id is not None:
        #     try:
        #         student = Student.objects.get(pk=student_id)
        #         serializer = StudentSerializer(student)
        #         return Response(serializer.data)
        #     except Student.DoesNotExist:
        #         return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        # else:
        #     queryset = Student.objects.all()
        #     serializer = StudentSerializer(queryset, many=True)
        #     return Response(serializer.data)

    # def get(self,request):
    #     form=Student.objects.all()
    #     p=Paginator(form,2)
    #     print(p)


        
    def post(self, request):
        data = request.data
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Student created"}, status=201)
        return Response(serializer.errors, status=400)
    
    def put(self, request, student_id):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, student_id):
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        student.delete()
        return Response({"message": "Student deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class StandardApi(APIView):

    def get(self, request):
        standards = Standard.objects.all()
        serializer = StandardSerializer(standards, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = StandardSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Standard created"}, status=201)
        return Response(serializer.errors, status=400)

    def put(self, request, standard_id):
        try:
            standard = Standard.objects.get(pk=standard_id)
        except Standard.DoesNotExist:
            return Response({"error": "Standard not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = StandardSerializer(standard, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, standard_id):
        try:
            standard = Standard.objects.get(pk=standard_id)
        except Standard.DoesNotExist:
            return Response({"error": "Standard not found"}, status=status.HTTP_404_NOT_FOUND)
        
        standard.delete()
        return Response({"message": "Standard deleted"}, status=status.HTTP_204_NO_CONTENT)
    
class StudentsByStandardApi(APIView):
    def get(self, request, standard_id):
        try:
            standard = Standard.objects.get(pk=standard_id)
            students = Student.objects.filter(standard=standard)
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)
        except Standard.DoesNotExist:
            return Response({"error": "Standard not found"}, status=status.HTTP_404_NOT_FOUND)

def index(request):
    all_students = Student.objects.all()
    return render(request, 'students_management/students.html', {'all_students': all_students})

def insert(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            rollno = request.POST.get('rollno')
            standard_id = request.POST.get('standard')  # Assuming standard is provided as ID
            course = request.POST.get('course')
            
            # Ensure all required fields are provided
            if name and rollno and standard_id:
                # Get the Standard object
                standard = Standard.objects.get(pk=standard_id)
                
                # Create and save the Student object
                member = Student(name=name, rollno=rollno, standard=standard, course=course)
                member.save()
                
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'message': 'Incomplete data provided.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)
    else:
        # Handle invalid request method
        return JsonResponse({'success': False, 'message': 'Method not allowed.'}, status=405)
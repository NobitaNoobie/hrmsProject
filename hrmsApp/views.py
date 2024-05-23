# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q, DateField
from datetime import date
from .models import Emp_Leave_Data, Staff_data

from .models import LeaveApplication
from .serializers import HrmsAppSerializer

from datetime import datetime
from django.db.models.functions import ExtractDay, Cast

from datetime import datetime
from django.db.models.functions import Cast
from django.db.models import DateField
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def wfh_frequency(request, employee_id):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        try:
            today_date = datetime.strptime(today_date_str, "%Y-%m-%d").date()
            sum = 0
            sumsq = 0
            num_gap_days_arr = []
            avg_leave_gaps = 0.0
            
            # query sets
            emp_wfh_leave_duration = Emp_Leave_Data.objects.filter(emp_id = employee_id , leave_from__lte = today_date , leave_type = 6).order_by('leave_from')
            emp_data = Staff_data.objects.get(staff_id = employee_id)
            
            # average
            for i in range(1, len(emp_wfh_leave_duration)):
                num_gap_days = abs(emp_wfh_leave_duration[i].leave_from - emp_wfh_leave_duration[i-1].leave_to).days
                num_gap_days_arr.append(num_gap_days)
                print(num_gap_days)
                sum += num_gap_days

            if len(emp_wfh_leave_duration)-1 != 0:
                avg_leave_gaps = sum / (len(emp_wfh_leave_duration) - 1)
            else:
                avg_leave_gaps = 0


            # variance and standard deviation
            std_in_wfh = 0.0
            for ele in num_gap_days_arr:
                sumsq += pow((ele - avg_leave_gaps),2)
            
            print(sumsq)
            
            if len(emp_wfh_leave_duration)-1 != 0:
                variance = sumsq / (len(emp_wfh_leave_duration) - 1)
                print(variance)
                std_in_wfh = round(pow(variance,0.5), 2)
            else:
                std_in_wfh = 0

            res = ""
            if std_in_wfh <= 7:
                res = "highly"
            elif std_in_wfh <= 15:
                res = "moderately"
            else:
                res = "less"

            return Response({'msg': f'{emp_data.firstname} {emp_data.lastname} takes WFH after {avg_leave_gaps} on an average. A standard deviation of {std_in_wfh} indicates that the person is {res} likely to follow this WFH pattern.', 'status':1})


        except Exception as e:
            return Response({'error': str(e) , 'status': 0})
        
        
@api_view(['GET'])
def leave_frequency(request, employee_id):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        try:
            today_date = datetime.strptime(today_date_str, "%Y-%m-%d").date()
            sum = 0
            sumsq = 0
            num_gap_days_arr = []
            avg_leave_gaps = 0.0
            
            # query sets
            emp_wfh_leave_duration = Emp_Leave_Data.objects.filter(emp_id = employee_id , leave_from__lte = today_date).exclude(leave_type = 6).order_by('leave_from')
            emp_data = Staff_data.objects.get(staff_id = employee_id)
            
            # average
            for i in range(1, len(emp_wfh_leave_duration)):
                num_gap_days = abs(emp_wfh_leave_duration[i].leave_from - emp_wfh_leave_duration[i-1].leave_to).days
                num_gap_days_arr.append(num_gap_days)
                print(num_gap_days)
                sum += num_gap_days

            if len(emp_wfh_leave_duration)-1 != 0:
                avg_leave_gaps = sum / (len(emp_wfh_leave_duration) - 1)
            else:
                avg_leave_gaps = 0


            # variance and standard deviation
            std_in_wfh = 0.0
            for ele in num_gap_days_arr:
                sumsq += pow((ele - avg_leave_gaps),2)
            
            print(sumsq)
            
            if len(emp_wfh_leave_duration)-1 != 0:
                variance = sumsq / (len(emp_wfh_leave_duration) - 1)
                print(variance)
                std_in_wfh = round(pow(variance,0.5), 2)
            else:
                std_in_wfh = 0

            res = ""
            if std_in_wfh <= 7:
                res = "highly"
            elif std_in_wfh <= 15:
                res = "moderately"
            else:
                res = "less"

            return Response({'msg': f'{emp_data.firstname} {emp_data.lastname} takes leaves after {avg_leave_gaps} on an average. A standard deviation of {std_in_wfh} indicates that the person is {res} likely to follow this leave pattern.', 'status':1})


        except Exception as e:
            return Response({'error': str(e) , 'status': 0})


@api_view(['GET'])
def leave_applications_on_date(request, date):
    if request.method == 'GET':
        try:
            today_date = datetime.strptime(date, "%Y-%m-%d").date()
            #print(today_date)

            # # all Emp_Leave_Data objects
            # objs = Emp_Leave_Data.objects.all()
            # for obj in objs:
            #     print(obj.date_of_request)

            print(Emp_Leave_Data.objects.annotate(request_date=Cast('date_of_request', DateField())).filter(request_date=today_date).get_queryset)
            leave_count = Emp_Leave_Data.objects.annotate(request_date=Cast('date_of_request', DateField())).filter(request_date=today_date).count()

            return Response({'employees applied for leave': leave_count, "status": 1})
        except Exception as e:
            return Response({'error': str(e), "status": 0})

#date_of_request is a DateTime field, when you directly compare using __date lookup, not converted to date object before comparison. 
#Cast converts DateTime field to DateField, converts to date object.  
  

@api_view(['GET'])
def leave_applications_on_today(request):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        
        try:
            today_date = datetime.strptime(today_date_str, "%Y-%m-%d").date()
            leave_count = Emp_Leave_Data.objects.annotate(request_date=Cast('date_of_request', DateField())).filter(request_date=today_date).count()

            return Response({'employees applied for leave today': leave_count, "status": 1})
        except Exception as e:
            return Response({'error': str(e), "status": 0})


@api_view(['GET'])
def num_employees_on_leave_on_day(request, date):
    if request.method == 'GET':
        try:
            today_date = datetime.strptime(date, "%Y-%m-%d").date()
            employees_on_leave = Emp_Leave_Data.objects.filter(Q(leave_from__lte = today_date) & Q(leave_to__gte = today_date))
            num_employees = employees_on_leave.count()

            #list of employees on leave today
            # -- SQL QUERY, LIST OF EMPLOYEES ON LEAVE TODAY-------------------------------------------- 
            # select staff_data.staff_id as 'List of employees on leave today' ,staff_data.firstname as 'First Name', staff_data.lastname as 'Last Name' from staff_data
            # join emp_leave_data on staff_data.staff_id = emp_leave_data.emp_id 
            # where emp_leave_data.leave_from <= curdate() and curdate() <= emp_leave_data.leave_to;

            # list_of_employees_on_leave = Staff_data.objects.filter(Q(staff_id__leave_from__lte=today_date) & Q(staff_id__leave__leave_to__gte=today_date)).distinct()

            list_of_employees_on_leave = Staff_data.objects.filter(staff_id__in= employees_on_leave.values('emp_id')).distinct()
            
            employee_data = []
            for employee in list_of_employees_on_leave:
                employee_info = {
                    'Staff Id': employee.staff_id,
                    'Name': f"{employee.firstname} {employee.lastname}"
                }
                employee_data.append(employee_info)
 
            response_data = {
                f'Number of employees on leave on {today_date}': num_employees,
                f'List of employees on leave on {today_date}': employee_data
            }
            return Response({"msg": response_data , "status":1})
        except Exception as e:
            return Response({"error":str(e), "status":0})


@api_view(['GET'])
def num_employees_on_leave_today(request):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', str(date.today())) #parameter is today's date by default

        try: 
            today_date = date.fromisoformat(today_date_str)
            #don't need to annotate and cast here because leave_from is a DateField. it will directly create a date object.
            employees_on_leave_query_set = Emp_Leave_Data.objects.filter(Q(leave_from__lte = today_date) & Q(leave_to__gte = today_date)) #query set is returned
            #you can generate the SQL query by doing .query on the query set. 
            print(employees_on_leave_query_set.query)
            employee_count = employees_on_leave_query_set.count()
            list_of_employees_on_leave = Staff_data.objects.filter(staff_id__in = employees_on_leave_query_set.values("emp_id")).distinct()

            employees_on_leave_data_array = []
            for employee in list_of_employees_on_leave:
                employee_info = {
                    "Staff id": employee.staff_id,
                    "Name": f"{employee.firstname} {employee.lastname}"
                }
                employees_on_leave_data_array.append(employee_info)

            response_data = {
                "Number of employees on leave today": employee_count,
                "List of employees on leave today: ": employees_on_leave_data_array}
            return Response({"msg": response_data, "status":1})
        except Exception as e:
            return Response({'error':str(e) , "status":0})


# @api_view(['GET'])
# def num_employees_on_leave_past_seven_days(request):
#     if request.method == 'GET':
#         today_date_str = request.GET.get('date', str(date.today()))

#         try:
#             today_date = date.fromisoformat(today_date_str)
#             #extract how many people were absent on each day of last week.


#             return 
#         except Exception as e:
#             return Response({"msg": f"On an average {count_week_avg} number of employees were on leave in the past week"})


#views are pyhton functions that take a request and return a web response, in this case an HttpResponse

#get all the employees, serialize them and return json
@api_view(['GET', 'POST'])
def employee_list(request):
    if request.method == 'GET':
        #get all the employees
        employees = LeaveApplication.objects.all()
        #serialize them
        serializer = HrmsAppSerializer(employees, many=True)
        #return json
        return JsonResponse(serializer.data, safe=False)
    
    elif request.method == 'POST':
        #to post a new employee
        #first deserialize the json data from the request
        #when request.data is used that means it is picking 'data' from the body
        #you can alternatively search using ModelClass.objects.get()
        deserializer = HrmsAppSerializer(data = request.data)
        #then check is the data is correct
        if deserializer.is_valid():
            deserializer.save()
            return Response({"data": deserializer.data, "message": "A new employee was added" ,"status": 201})
        

        


@api_view(['GET'])
def employeehome(request, employee_id):
    try:
        employee = LeaveApplication.objects.get(pk=employee_id)
    except LeaveApplication.DoesNotExist:
        return Response({"message":"User not found", "status":0})
    
    if request.method == 'GET':
        return Response({"data":employee.employee_name, "status":1})


@api_view(['GET', 'PUT'])
def applyLeave(request, employee_id):
    try:
        #find the data corresponding to the employee id(primary key)
        #store this data in a variable
        employee = LeaveApplication.objects.get(pk=employee_id)
    except LeaveApplication.DoesNotExist:
        return Response({"message":"Employee not found", "status":404})
        
    if request.method == 'GET':    
        #get the employee ....done above 
        #serialize them
        serializer = HrmsAppSerializer(employee)
        #return response
        return Response({"employee data":serializer.data})

    if request.method == 'PUT':
        if employee.has_applied == True:
            return Response({"message":"You have already applied for leave"})
        else:
            employee.has_applied = True
            print("herte", employee.leave_type)
            if employee.leave_type == 'Restricted Holiday':
                if(employee.app_leave_rh >= employee.available_leave_balance_rh):
                    return Response({"message": "Oops! Number of RH leaves applied exceeds your remaining number of leaves"})
                else:
                    employee.available_leave_balance_rh -= employee.app_leave_rh
                    employee.save()
                    return Response({"message":"Leave application(RH) successfull! HAPPY HOLIDAYS!", "status":200})
                
            elif employee.leave_type == 'CL':
                if(employee.app_leave_cl >= employee.available_leave_balance_cl):
                    return Response({"message": "Oops! Number of CL leaves applied exceeds your remaining number of leaves"})
                else:
                    employee.available_leave_balance_cl -= employee.app_leave_cl
                    employee.save()
                    return Response({"message":"Leave application(CL) successfull! HAPPY HOLIDAYS!", "status":200})
                
            elif employee.leave_type == 'EL':
                if(employee.app_leave_el >= employee.available_leave_balance_el):
                    return Response({"message": "Oops! Number of EL leaves applied exceeds your remaining number of leaves"})
                else:
                    employee.available_leave_balance_el -= employee.app_leave_el
                    employee.save()
                    return Response({"message":"Leave application(EL) successfull! HAPPY HOLIDAYS!", "status":200})
                
            # if(employee.app_leave >= employee.available_leave_balance):
            #     return Response({"message": "Oops! Number of leaves applied exceeds your remaining number of leaves"})
            # else:
            #     employee.available_leave_balance -= employee.app_leave
            #     employee.save()
            #     return Response({"message":"Leave application successfull! HAPPY HOLIDAYS!", "status":200})

        




# def index(request):
#     employee_id = 'GSTN053'
#     print("leaveapp : ",LeaveApplication.objects.all())
#     employee = LeaveApplication.objects.filter(employee_id = employee_id)
#     print("emp",employee)
    
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         app_leave = request.POST.get('app_leave')
#         num_days = app_leave

#         if employee.available_leave_balance >= num_days:
#             employee.available_leave_balance -= num_days
            
#             employee.start_date = start_date
#             employee.end_date = end_date
#             employee.save()

#             return render(request, 'hrmsApp/index.html', {'employee_id': employee_id, 'success_message': 'Leave applied successfully!'})
#         else:
#             return render(request, 'hrmsApp/index.html', {'employee_id': employee_id, 'error message':'Your leave balance is not enough'})
#    return render(request, 'hrmsApp/index.html', {'employee_id': employee_id})


# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.utils import timezone

from hrmsApp.models import LeaveApplication
from hrmsApp.serializers import HrmsAppSerializer

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


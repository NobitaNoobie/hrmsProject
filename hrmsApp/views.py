# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Q, DateField, F
from datetime import date, timedelta
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

from .forms import UserInfoForm

def regform(request):
    form = UserInfoForm()
    context = {'form':form}
    return render(request, "hrmsApp/index.html", context=context)

def count_leave_instances_till_date(date, emp_id):
    leave_instances_count = Emp_Leave_Data.objects.filter(emp_id = emp_id , leave_from__lte = date).count()
    return leave_instances_count

def count_all_leave_instances(emp_id):
    leave_instances_count = Emp_Leave_Data.objects.filter(emp_id = emp_id).count()
    return leave_instances_count

def get_staff_data(emp_id):
    emp_data = Staff_data.objects.get(staff_id = emp_id)
    return emp_data

# accepts a datetime argument to_day
def get_weekday(to_day):
    #self-defined function
    # one weekday value needs to be given, in this case from_day's weekday value is given
    from_day_str = "1999-08-10" #my birthday
    from_day = datetime.strptime(from_day_str , "%Y-%m-%d")

    diff = abs(to_day - from_day) # datetime values
    rem = diff.days % 7
    from_day_val = 1 # known value
    if from_day < to_day:
        to_day_val = (from_day_val + rem) % 7
    else:
        to_day_val = (from_day_val - rem) % 7
        
    return to_day_val

def get_weekends_count(start_date , end_date):
            #self-defined function tiyasa khan
    #find the number of weekends between start_date and end_date
    #NOTE:::: START DATE < END DATE ALWAYS
            start_date_weekday = get_weekday(start_date)
            end_date_weekday = get_weekday(end_date)
            first_day_of_week_dayoftheweek = start_date_weekday
            total_days = (end_date - start_date).days + 1 #caution

            div = int(total_days / 7)
            rem = int(total_days % 7)

            num_weekends = div * 2
            
            for i in range(rem):
                if(first_day_of_week_dayoftheweek + i) % 7 in (5,6):
                    num_weekends += 1

            # print("WEEKENDS NO.",num_weekends)
            num_weekdays = (total_days - num_weekends)
            # print("WEEKDAYS NO.", num_weekdays)

            # # Exclude holidays from weekdays
            # for holiday in holidays:
            #     if start_date <= holiday <= end_date and holiday.weekday() not in (5, 6):
            #         num_weekdays -= 1

            return num_weekends



# absenteeism rate 
# monthly absenteeism rate. month as in not 30 days duration, but 01, 02(feb),... like this
# quarterly absenteeism rate - 3 months
# find the increase or decrease in company-wide rate of absenteeism compared to: previous month, previous quarter,... etc(open to suggestions)

# absenteeism rate = (total number of absent days for N employees) / (N * number of working days in a given time period)

# N = number of employees

#curent month and its comparison with the previous month
# or, monthly -> a chart?

@api_view(['GET'])
def absenteeism_rate(request):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        # today_date_str = "2024-06-3"
        try:
            # NUMBER OF WEEKENDS CALCULATION --------------------------------------------------------------------------------------------
            today_date = datetime.strptime(today_date_str, "%Y-%m-%d")
            curr_month = today_date.month
            curr_year = today_date.year

            start_date_str = f"{str(curr_year)}-{str(curr_month)}-01"
            print(start_date_str)
            # now i will convert this string to datetime object to find which day of the week, the starting of the current month was
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")

            count = get_weekends_count(start_date , today_date)
            print('Number of weekends in the month:', count)


            start_date_weekday = get_weekday(start_date)
            # another method is to use the builtin weekday() method of datetime, as shown below:
            # start_date_weekday = start_date.weekday()
            print('Start day of the month weekday',start_date_weekday)

            #today_date_dayoftheweek = today_date.weekday()
            today_date_dayoftheweek = get_weekday(today_date)

            first_day_of_week_dayoftheweek = start_date_weekday

            total_days = today_date.day 

            div = int(total_days / 7)
            rem = int(total_days % 7)

            num_weekends = div * 2
            
            for i in range(rem):
                if(first_day_of_week_dayoftheweek + i) % 7 in (5,6):
                    num_weekends += 1

            # if first_day_of_week_dayoftheweek == 6:
            #     num_weekends += 2
            # elif first_day_of_week_dayoftheweek == 5:
            #     num_weekends += 1

            #find the number of weekends in the remaining number of days
            

            print("WEEKENDS NO.",num_weekends)
            num_weekdays = (total_days - num_weekends)
            print("WEEKDAYS NO.", num_weekdays)
            

            #print(today_date.weekday())






            # TOTAL NUMBER OF HOLIDAYS CALCULATIONS-------------------------------------------------------------------------------------
            total_leave_count = 0
            leave_data = Emp_Leave_Data.objects.filter(
                leave_to__gte=start_date,
                leave_from__lte=today_date
            )
            
            print('Query set generated. The number of objects fetched:', len(leave_data))

            for leave in leave_data:
                leave_f = datetime.combine(leave.leave_from, datetime.min.time())
                leave_start_date = max(leave_f, start_date) 
                #print(leave_start_date)

                leave_t = datetime.combine(leave.leave_to, datetime.min.time())
                leave_end_date = min(leave_t, today_date)  # Only consider up to today
                #print(leave_end_date)
            
                leave_days = (leave_end_date - leave_start_date).days + 1
                num_weekends = get_weekends_count(leave_start_date, leave_end_date)
                leave_days -= num_weekends
                total_leave_count += leave_days
                

            print("Total companywide leaves in the current month = ", total_leave_count, " days")
            count_total_employees = len(Staff_data.objects.all())
            print(count_total_employees)
            if count_total_employees * num_weekdays > 0:
                absent_rate = round((total_leave_count * 100)/(count_total_employees * num_weekdays) , 2)
                return Response({'msg':absent_rate, 'status': 1})
            else:
                return Response({'msg':'Division by 0', 'status':0})
            # return Response({'msg':f"The absenteeism rate for {today_date.strftime('%B')} is {absent_rate}%", 'status': 1})
            

        except Exception as e:
            return Response({'msg': str(e) , 'status':1})


def monthly_absent_rate(month_val, year_val):
            curr_month_val = month_val #MM integer value for months, ranging from Jan(1) to Dec(12)
            curr_year_val = year_val #YYYY
            
            day1 = datetime.strptime(f"{curr_year_val}-{curr_month_val}-01", "%Y-%m-%d") #converting 1st day of curr_month into datetime object
            print('start day of curr month = ', day1)
            if curr_month_val == 12:
                day2 = datetime.strptime(f"{curr_year_val+1}-01-01", "%Y-%m-%d")
            else:
                day2 = datetime.strptime(f"{curr_year_val}-{curr_month_val+1}-01", "%Y-%m-%d") #converting 1st day of NEXT month into datetime object
            print('start day of next month = ',day2)
            total_days_in_month = (day2 - day1).days #number of days in the given month
            print('total days in month = ', total_days_in_month)
            print(get_weekends_count(day1, day2))
            num_working_days_in_month = total_days_in_month - get_weekends_count(day1, day2)
            print('number of working days in month = ', num_working_days_in_month)

            companywide_absents_in_month = Emp_Leave_Data.objects.filter(leave_to__gte = day1, leave_from__lte = day2)
            companywide_absents_in_month_count = 0

            for leave in companywide_absents_in_month:
                #someone might take a leave from 29/4/2024 to 3/5/2024
                #in this case 2 leaves are in the month of April and rest 3 leaves are in the month of May
                #we need to correctly handle this edge case, where we define leave_start date and leave_end_date
                #in this case to correctly calculate the number of leaves in May, the leave_start_date = 1/5/2024
                leave_f = datetime.combine(leave.leave_from, datetime.min.time())
                leave_start_date = max(leave_f, day1)  
                print(leave_start_date)

                leave_t = datetime.combine(leave.leave_to, datetime.min.time())
                leave_end_date = min(leave_t, day2) 
                print(leave_end_date)
                #------------------------------------------------------------------------------------------------

                #find number of days elapsed between leave_start_date and leave_end_date
                #we need to subtract the number of weekends between leave_start_date and leave_end_date, because we don't want to...
                #...include weekends in our leave days
                days_between = (leave_end_date - leave_start_date).days + 1
                print('days between = ', days_between)
                weekends_between = get_weekends_count(leave_start_date, leave_end_date)
                leaves_between = days_between - weekends_between
                companywide_absents_in_month_count += leaves_between
            
            print(f'company wide absent days in {curr_month_val} = ',companywide_absents_in_month_count)
            num_employees = len(Staff_data.objects.all())
            print("num employees", num_employees)
            print("num working days", num_working_days_in_month)
            #absent_rate, even though a variable in the ifelse block, has a scope global to the function.
            #scopes within ifelse blocks dont count as local, as it would have in other programming languages, like JAVA
            if num_employees > 0 & num_working_days_in_month == 0:
                absent_rate = round(((companywide_absents_in_month_count * 100) / (num_employees * num_working_days_in_month)) , 2)
            else:
                absent_rate = 0

            return absent_rate
        

@api_view(['GET'])
def absenteeism_rate_monthly (request, month_val, year_val):
    if request.method == 'GET':
        try:
            curr_month_val = month_val #MM integer value for months, ranging from Jan(1) to Dec(12)
            curr_year_val = year_val #YYYY
            day1 = datetime.strptime(f"{curr_year_val}-{curr_month_val}-01", "%Y-%m-%d")

            curr_absent_rate = monthly_absent_rate(month_val, year_val)

            prev_month_val = (month_val - 1) if curr_month_val > 1 else 12
            prev_year_val = year_val if curr_month_val > 1 else year_val - 1
            prev_absent_rate = monthly_absent_rate(prev_month_val, prev_year_val)

            diff = round((prev_absent_rate - curr_absent_rate) , 2)

            return Response({'msg':f"The absenteeism rate for the month of {day1.strftime('%B')} is {curr_absent_rate}%, which is {'greater' if diff > 0 else 'lower'} than the last month by {diff}%", 'status': 1})
        except Exception as e:
            return Response({'msg': str(e) , 'status':0})
        
@api_view(['GET'])
def absenteeism_rate_relative (request, month_val, year_val):
    if request.method == 'GET':
        try:
            curr_month_val = month_val #MM integer value for months, ranging from Jan(1) to Dec(12)
            print(curr_month_val)
            curr_year_val = year_val #YYYY
            curr_absent_rate = monthly_absent_rate(month_val, year_val)
            print("curr absent rate",curr_absent_rate)

            prev_month_val = (month_val - 1) if curr_month_val > 1 else 12
            prev_year_val = year_val if curr_month_val > 1 else year_val - 1
            prev_absent_rate = monthly_absent_rate(prev_month_val, prev_year_val)
            print("Prev absent rate",prev_absent_rate)

            diff = round((curr_absent_rate - prev_absent_rate) , 2)

            return Response({'msg':f"{diff} % than last month",'diff': diff, 'curr':curr_absent_rate, 'prev':prev_absent_rate, 'status': 1})
        except Exception as e:
            return Response({'msg': str(e) , 'status':0})


month_val = {
    1: 'Januray',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}    


@api_view(['GET'])
def num_employees_on_leave_monthly(request):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        print("TODAYYYYYY", today_date_str)
        try:
            today_date = datetime.strptime(today_date_str, '%Y-%m-%d')
            curr_month = today_date.month
            curr_year = today_date.year
            emp_list = Emp_Leave_Data.objects.filter(Q(leave_from__lte=F('leave_to')) & Q(leave_to__month__gte = curr_month) & Q(leave_from__month__lte = curr_month)).values("emp_id")
            num = emp_list.distinct().count()
            print(emp_list)
            staff_detail_list = Staff_data.objects.filter(staff_id__in = emp_list.values("emp_id")).distinct()
            staff_details_list_arr = []
            for emp in staff_detail_list:
                employee_info = {
                    'Staff_Id': emp.staff_id,
                    'Name': f"{emp.firstname} {emp.lastname}"
                }
                staff_details_list_arr.append(employee_info)

            return Response({'msg': num, 'list':staff_details_list_arr, 'status': 1})
        except Exception as e:
            return Response({'msg': str(e), 'status': 0})

@api_view(['GET'])
def absenteeism_rate_list(request, year):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        try: 
            today_date = datetime.strptime(today_date_str , "%Y-%m-%d")
            curr_month = today_date.month
            curr_year = today_date.year
    
            if year == curr_year:
                absent_rate_list = []
                #for i in range(1,5) -> for(int i=1, i<5, i++)
                for month in range(1,curr_month+1):
                    curr_absent_rate = monthly_absent_rate(month, curr_year)
                    absent_rate_list.append({
                        'month': month_val.get(month),
                        'rate': f'{curr_absent_rate} %',
                    })
                response_data = {
                    f'Monthly rate of absenteeism for the year {year}:': absent_rate_list,
                }
                return Response({'msg': response_data, 'status':1})
                        
            elif year < curr_year:
                absent_rate_list = []
                #for i in range(1,5) -> for(int i=1, i<5, i++)
                for month in range(1, 13):
                    curr_absent_rate = monthly_absent_rate(month, year)
                    absent_rate_list.append({
                        'month': month_val.get(month),
                        'rate': curr_absent_rate,
                    })

                response_data = {
                    f'Monthly rate of absenteeism for the year {year}: ': absent_rate_list,
                }
                return Response({'msg': response_data, 'status':1})
                #return Response({'msg':f'List of monthly absenteeism rates for the year {curr_year}', 'list': f'{absent_rate_list}', 'status':1})

            else:
                return Response({'msg':'Invalid year', 'status': 0})

        except Exception as e:
            return Response({'msg':str(e) , 'status':0})
            
@api_view(['GET'])
def num_absentees_future(request):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        print(today_date_str)
        try:
            today_date = datetime.strptime(today_date_str , "%Y-%m-%d").date()

            currmonth = today_date.month
            curryear = today_date.year
            if currmonth == 1 | currmonth == 3 | currmonth == 5 | currmonth == 7 | currmonth == 8 | currmonth == 10 | currmonth == 12:
                end_date_str = f"{curryear}-{currmonth}-31"
            elif currmonth == 2:
                if curryear % 4 == 0:
                    end_date_str = f"{curryear}-{currmonth}-29"
                else:
                    end_date_str = f"{curryear}-{currmonth}-28"
            else:
                end_date_str = f"{curryear}-{currmonth}-30"
            print(end_date_str)
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            leave_instances = Emp_Leave_Data.objects.filter(leave_from__lte = end_date , leave_to__gte = today_date)
            print(len(leave_instances))
            arr = []
            for leave in leave_instances:
                if arr.__contains__(leave.emp_id) == False:
                    arr.append(leave.emp_id)
            num = len(arr)
            
            # return Response({'msg': f"Upcoming number of absentees in {month_val.get(currmonth)} is: {num}",'status': 1})
            return Response({'msg': num,'status': 1})
        except Exception as e:
            return Response({'msg': str(e) , 'status':0})


@api_view(['GET'])
def leave_rejection_rate(request, employee_id):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        try:
            today_date = datetime.strptime(today_date_str, "%Y-%m-%d").date()
            num_leave_instances = count_all_leave_instances(employee_id)
            print('Number of leave instances =', num_leave_instances)
            num_rejected_leaves = Emp_Leave_Data.objects.filter(emp_id = employee_id, approval_status = 0).count()
            leave_rej_rate = 0
            if num_rejected_leaves >= 1:
                leave_rej_rate = round((num_rejected_leaves*100)/num_leave_instances, 2)

            emp_data = get_staff_data(employee_id)

            if num_leave_instances == 0:
                return Response({'msg':f'As of {today_date.strftime("%dth %B %Y")}, {emp_data.firstname} {emp_data.lastname} has not taken any leaves' , 'status':1})
            else:
                return Response({'msg':f'As of {today_date.strftime("%dth %B %Y")}, {leave_rej_rate}% of {emp_data.firstname} {emp_data.lastname}\'s leaves have been rejected.' , 'status':1})
            

        except Exception as e:
            return Response({'msg': str(e), 'status': 0})


# improve the below api later, find out how to compare date-time field with date field and document it for future reference.

@api_view(['GET'])
def planned_unplanned_percentage(request, employee_id):
    if request.method == 'GET':
        today_date_str = request.GET.get('date', datetime.today().strftime('%Y-%m-%d'))
        try:
            today_date = datetime.strptime(today_date_str, "%Y-%m-%d").date()
            count_total_leave_instances = count_all_leave_instances(employee_id)
            count_planned_leaves = Emp_Leave_Data.objects.filter(emp_id = employee_id, leave_from__gte = 'date_of_request'.date()).count()
            planned_leave_percent = (count_planned_leaves*100)/count_all_leave_instances
            unplanned_leave_percent = 100 - planned_leave_percent
            return Response({'msg':'' , 'status':1})
        except Exception as e:
            return Response({'msg': str(e) , 'status': 0})
        
def unplanned_leaves_count():
    total_leaves = Emp_Leave_Data.objects.all().count()
    count_unplanned_leaves = round(Emp_Leave_Data.objects.annotate(request_date=Cast('date_of_request', DateField())).filter(leave_from__lte=F('request_date')).count() / total_leaves * 100)
    count_planned_leaves = round((100 - count_unplanned_leaves))
    return [count_unplanned_leaves , count_planned_leaves]
        
@api_view(['GET'])
def planned_leaves(request):
    if request.method == 'GET':
        try:
            count_planned_leaves = unplanned_leaves_count()[1]
            return Response({'msg': count_planned_leaves , 'status': 1})
        except Exception as e:
            return Response({'msg': str(e) , 'status': 0})

@api_view(['GET'])
def unplanned_leaves(request):
    if request.method == 'GET':
        try:
            count_unplanned_leaves = unplanned_leaves_count()[0]
            return Response({'msg': count_unplanned_leaves , 'status': 1})
        except Exception as e:
            return Response({'msg': str(e) , 'status': 0})

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
            emp_data = get_staff_data(employee_id)
            
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

            print(avg_leave_gaps)


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

            # added round(average) here because if we add round before during calculations, the other calcs like variation std will be affected
            if len(emp_wfh_leave_duration) > 1:
                return Response({'msg': f'{emp_data.firstname} {emp_data.lastname} takes WFH after {round(avg_leave_gaps)} days on an average. A standard deviation of {std_in_wfh} indicates that the person is {res} likely to follow this WFH pattern.', 'status':1})
            elif len(emp_wfh_leave_duration) == 0:
                return Response({'msg': f'As of {today_date.strftime("%dth %B %Y")}, {emp_data.firstname} {emp_data.lastname} has not taken any WFH', 'status': 1})
            else:
                return Response({'msg': f'As of {today_date.strftime("%dth %B %Y")}, {emp_data.firstname} {emp_data.lastname} has taken only 1 WFH. Not enough data to predict leave frequency.', 'status':1})

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
            emp_data = get_staff_data(employee_id)
            
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

            if len(emp_wfh_leave_duration) > 1:
                return Response({'msg': f'{emp_data.firstname} {emp_data.lastname} takes leaves after {round(avg_leave_gaps)} days on an average. A standard deviation of {std_in_wfh} indicates that the person is {res} likely to follow this leave pattern.', 'status':1})
            elif len(emp_wfh_leave_duration) == 0:
                return Response({'msg': f'As of {today_date.strftime("%dth %B %Y")}, {emp_data.firstname} {emp_data.lastname} has not taken any leaves.', 'status': 1})
            else:
                return Response({'msg': f'As of {today_date.strftime("%dth %B %Y")}, {emp_data.firstname} {emp_data.lastname} has taken only 1 leave. Not enough data to predict leave frequency.', 'status':1})

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
            print('today ', today_date)
            #week_before_date = (today_date - 7)
            #use timedelta to subtract 7, do not directly subtract 7 because date type will not be compatible with int type
            week_before_date = today_date - timedelta(days=7)
            print("week before ", week_before_date)
            leave_count = Emp_Leave_Data.objects.annotate(request_date=Cast('date_of_request', DateField())).filter(request_date=today_date).count()
            leave_count_last_week = Emp_Leave_Data.objects.annotate(request_date = Cast('date_of_request', DateField())).filter(request_date__gte = week_before_date , request_date__lt = today_date).count()
            diff = leave_count - leave_count_last_week

            #list of leave applications today
            leave_applications_list = Emp_Leave_Data.objects.annotate(request_date = Cast('date_of_request', DateField())).filter(request_date = today_date)
            staff_leave_applications = Staff_data.objects.filter(staff_id__in = leave_applications_list.values("emp_id")).distinct()
            staff_leave_applications_arr = []
            for emp in staff_leave_applications:
                employee_info = {
                    'Staff_id': emp.staff_id,
                    'Name': f"{emp.firstname} {emp.lastname}"
                }
                staff_leave_applications_arr.append(employee_info)
            
            return Response({"msg": leave_count, 'diff':diff , 'list': staff_leave_applications_arr ,"status": 1})
        except Exception as e:
            return Response({'error': str(e), "status": 0})            


@api_view(['GET'])
def num_employees_on_leave_on_day(request, date):
    if request.method == 'GET':
        try:
            today_date = datetime.strptime(date, "%Y-%m-%d").date()
            employees_on_leave = Emp_Leave_Data.objects.filter(Q(leave_from__lte = today_date) & Q(leave_to__gte = today_date)).values('emp_id')
            num_employees = employees_on_leave.distinct().count()

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
                    'Staff_Id': employee.staff_id,
                    'Name': f"{employee.firstname} {employee.lastname}"
                }
                employee_data.append(employee_info)
 
            # response_data = {
            #     f'Number of employees on leave on {today_date}': num_employees,
            #     f'List of employees on leave on {today_date}': employee_data
            # }
            # return Response({"msg": response_data , "status":1})
            return Response({"msg": num_employees , 'list':employee_data, "status":1})
        except Exception as e:
            return Response({"error":str(e), "status":0})


@api_view(['GET'])
def num_employees_on_leave_today(request):
    if request.method == 'GET':
        print("request receivedddddd")
        today_date_str = request.GET.get('date', str(date.today())) #parameter is today's date by default

        try: 
            today_date = date.fromisoformat(today_date_str)
            #don't need to annotate and cast here because leave_from is a DateField. it will directly create a date object.
            employees_on_leave_query_set = Emp_Leave_Data.objects.filter(Q(leave_from__lte = today_date) & Q(leave_to__gte = today_date)).values('emp_id') #query set is returned
            #you can generate the SQL query by doing .query on the query set. 
            print(employees_on_leave_query_set.query)
            employee_count = employees_on_leave_query_set.distinct().count()
            list_of_employees_on_leave = Staff_data.objects.filter(staff_id__in = employees_on_leave_query_set.values("emp_id")).distinct()
            employees_on_leave_data_array = []
            for employee in list_of_employees_on_leave:
                 employee_info = {
                     "Staff_id": employee.staff_id,
                     "Name": f"{employee.firstname} {employee.lastname}"
                 }
                 employees_on_leave_data_array.append(employee_info)

            # response_data = {
            #     "Number of employees on leave today": employee_count,
            #     "List of employees on leave today: ": employees_on_leave_data_array}
            print({employee_count})
            # return Response({"msg": f"Number of employees on leave today: {employee_count}", "status":1})
            return Response({"msg": employee_count, 'list': employees_on_leave_data_array, "status":1})
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


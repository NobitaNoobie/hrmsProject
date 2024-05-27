# here i test out new functions that I come up with whether they are returing the correct result, before writing them in the code
from datetime import datetime
weekdays = {
        0: "Monday",
        1: "Tuesday",
        2: "Wednesday",
        3: "Thursday",
        4: "Friday",
        5: "Saturday",
        6: "Sunday"
    }

def get_weekends_count(start_date , end_date, holidays):
    #find the number of weekends between start_date and end_date
    #NOTE:::: START DATE < END DATE ALWAYS
            start_date_weekday = start_date.weekday()
            end_date_weekday = end_date.weekday()
            first_day_of_week_dayoftheweek = start_date_weekday
            total_days = (end_date - start_date) #caution

            div = total_days // 7
            rem = total_days % 7

            num_weekends = div * 2
            
            for i in range(rem):
                if(first_day_of_week_dayoftheweek + i) % 7 in (5,6):
                    num_weekends += 1

            print("WEEKENDS NO.",num_weekends)
            num_weekdays = (total_days - num_weekends)
            print("WEEKDAYS NO.", num_weekdays)

            # Exclude holidays from weekdays
            for holiday in holidays:
                if start_date <= holiday <= end_date and holiday.weekday() not in (5, 6):
                    num_weekdays -= 1

            return num_weekdays

# Input
from_day_str = input("Enter the date (YYYY-MM-DD): ")
from_day = datetime.strptime(from_day_str, "%Y-%m-%d")

# Input
to_day_str = input("Enter the date (YYYY-MM-DD): ")
to_day = datetime.strptime(to_day_str, "%Y-%m-%d")

holi = [from_day_str]

print(get_weekends_count(from_day , to_day, holi))
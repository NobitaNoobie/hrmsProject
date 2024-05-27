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

def get_weekday(to_day):
    # one weekday value needs to be given, in this case from_day's weekday value is given
    from_day_str = "1999-08-10"
    from_day = datetime.strptime(from_day_str , "%Y-%m-%d")

    diff = abs(to_day - from_day) # datetime values
    rem = diff.days % 7
    from_day_val = 1 #known value
    if from_day < to_day:
        to_day_val = (from_day_val + rem) % 7
    else:
        to_day_val = (from_day_val - rem) % 7
        
    return to_day_val

# Input
from_day_str = input("Enter the date (YYYY-MM-DD): ")


# input strings to datetime objects
from_day = datetime.strptime(from_day_str, "%Y-%m-%d")
to_day_weekday = get_weekday(from_day)
print(f"The weekday for the end date is: {to_day_weekday} {weekdays.get(to_day_weekday)}(0=Monday, 6=Sunday)")

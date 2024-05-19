#assignment_2
import requests
from geopy.geocoders import Nominatim 
from menu import the_report, show_menu, get_report_type, get_user_choices


#define the user_agent and timeout limit
geolocator = Nominatim(user_agent = "weather")

#pass in the location variable and target days
#catch errors if user input something wrong
try:
    address = input("Enter your address to forecast ")
    location = geolocator.geocode(address)
    if location:
        print(f"location found: {location}")
    else:
        print("Invaild input, please enter existing address or city, etc.")
        exit()
except Exception as e:
    print(f"Oops.. somthing went wrong... Error msg:{e}")

#doing error dectect for 'target_time'
try:
    target_time = int(input("Enter desired days. maximum 16 days. "))
 
    if not (0 < target_time < 16):
        raise ValueError("Invaild number. Min input 1 day, max 16 days")

#if user enter something that's not int
except ValueError as ve:
    print(ve)
    exit()

#gerneral exception
except Exception as e:
     print(f"Oops.. somthing went wrong... Error msg:{e}")


#set variables for results 
longs = location.longitude
lats = location.latitude


#use the longs and als and target_time to get the weather forecast
parameters = {
    "latitude": lats,
    "longitude": longs,
    "hourly": "apparent_temperature,precipitation,dewpoint_2m,wind_speed_10m,visibility",
    "forecast_days": target_time,
}

response = requests.get(url= "https://api.open-meteo.com/v1/forecast?", params= parameters)



def main():    

    #pass the functions and assign the vars
    show_menu()
    selects =  get_user_choices()
    report_type = get_report_type()

    #reassign the list
    hourly_data = response.json().get("hourly", [])
    report = the_report(target_time, hourly_data, selects, report_type)



    # #print out the results
    print(f"Your forecast location: {location}")
    print(f"Your choices:  {selects}")
    print(f"Your report type: {report_type}")
    print(f"Here's your generated report: \n{report}")
    
#check if the main code that is running 
if __name__ == "__main__":
    main()
from datetime import datetime,timedelta

#functions

#for collectiong the values from the variables
def collect_item(hourly_data,x,i):
    item = hourly_data[x][i]
    return item

#gather the values and make the average easy to excute
def cal_average(hourly_data, data_range, variable):
       
    tot_value = 0
    #sum up the values
    for i in data_range:
        tot_value += hourly_data[variable][i]

     #average with len        
    avg_value = tot_value / len(data_range)

    return avg_value

#the menu for user's choice
def show_menu():
    print("Menu:")
    print("Form your personalize weather report!")
    print("1. Apparent temperature ")
    print("2. Precipitation")
    print("3. Dewpoint")
    print("4. Wind speed")
    print("5. Visibility")
    print("6. All of above")
    print("type 'esc' to leave")

#collect user choices 
def get_user_choices():
    while True:
        print("Enter your choices. (eg., 1,3,5)")
        vari_input = input().strip().lower()
    
        #check if user entering the correctly
        if not (char.isdigit() or char == ',' for char in vari_input):
            raise ValueError("Invaild, please enter choices with comma.")
              
        #put user's choices into list 
        try:
            
            #split the input into numbers
            variables = [int(option) for option in vari_input.split(",")]

            #prevent user input somthing like '1,2,6' by checking is there an overlap
            if set(variables).intersection({1,2,3,4,5}) and 6 in variables:
                raise ValueError("Invaild combination, please try again.")
            return variables
        
        except ValueError:
            print("Invalid input. Please enter valid options")
            break

#diff style for report 
def get_report_type():
    print("enter 'h' for hourly data or 's' for a summarized report ")
    report_t = input()
    if report_t == 'h':
        return "hourly"
    elif report_t == 's':
        return "summary"
    else:
        print("Invalid choice, defaulting to hourly report")
        return "hourly"

#where we generate the report
def the_report(target_time, hourly_data, choices, report_type):

    #create an empty list first
    report={}

    #key:value
    options = {
        1: "apparent_temperature",
        2: "precipitation",
        3: "dewpoint_2m",
        4: "wind_speed_10m",
        5: "visibility"
    }

    #include all for 6_all above
    if 6 in choices:
        choices = list(options.keys())


    #if the user choose hourly style, use the 'collect_item' to get the data 
    #put the data in a list
    if report_type == "hourly":
        for choice in choices:
            variable_data = []

            for i in range(len(hourly_data["time"])):
                #seperate the date and time
                format_dt = datetime.fromisoformat(hourly_data["time"][i])
                variable_data.append({
                    "Date": format_dt.strftime("%Y-%m-%d"),
                    "Time": format_dt.strftime("%H:%M"),
                    "data": collect_item(hourly_data, options[choice],i)
                    })
                report[options[choice]] = variable_data

    #if the user shooce summary, use 'cal_average' to get the data
    #put them into vars and then into list
    elif report_type == "summary":
        #seperate the date and time
        format_dt = datetime.now().date()
        
        summ_dict = {}

        for choice in choices:
            day = list(range(6,18))
            night = (list(range(0,6)) + list(range(18,24)))
            
            #create a dict for each variables
            vari_summ = {}
 
            for i in range(target_time):
                current = format_dt + timedelta(days= i)     
                day_value = round((cal_average(hourly_data,day, options[choice])),2)
                night_value = round((cal_average(hourly_data,night, options[choice])),2)
            
                vari_summ[f"{options[choice]}_Day_{i+1}"] = {
                    "Date": current.strftime("%Y-%m-%d"),
                    "Daytime": day_value,
                    "Nightime": night_value
                }
            summ_dict[options[choice]] = vari_summ
        report = summ_dict

    return report
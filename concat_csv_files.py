import numpy as np
import pprint
import os
import csv
from datetime import datetime
import time
from matplotlib import pyplot as plt

concat_csv = []

for file in os.listdir('/Users/michaelshamoun/Documents/qqq_data'):
    with open('/Users/michaelshamoun/Documents/qqq_data/'+file, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                #print(f'Column names are {", ".join(row)}')
                line_count += 1
            #print(f'\t{row["name"]} works in the {row["department"]} department, and was born in {row["birthday month"]}.')
            concat_csv.append(row)
            line_count += 1
        #print(f'Processed {line_count} lines.')

#sorted_data = sorted(concat_csv, key=lambda d: d['Date']) 

#date_temp = "12/21/2021"
#print(time.mktime(datetime.strptime(date_temp, "%m/%d/%Y").timetuple()))

sorted_data = sorted(concat_csv, key=lambda d: datetime.strptime(d['Date'], "%m/%d/%Y")) 

#pretty_dict_str = pprint.pformat(sorted_data)
#print(pretty_dict_str)

#num_days = len(sorted_data)
#print(num_days)

percent_change_data = []

previous_close = float(sorted_data[0]['Close'])

for day in sorted_data[1:]:
    date  = day['Date']
    close = float(day['Close']) 

    perc_change = (close / previous_close) - 1
    previous_close = close
    
    temp_dict = {}
    temp_dict['Date']           = date
    temp_dict['Percent Change'] = perc_change
    temp_dict['Close']          = close

    percent_change_data.append(temp_dict)

#pretty_dict_str = pprint.pformat(percent_change_data)
#print(pretty_dict_str)

total_value_list        = []
total_value_lev_list    = []
rel_total_value_list    = []

starting_position   = 100
adding_position     = 100

total_position      = starting_position
total_position_lev  = starting_position

previous_close      = float(sorted_data[0]['Close'])
previous_close_lev  = float(sorted_data[0]['Close'])

total_shares        = 100.0/previous_close
total_shares_lev    = total_shares

x_dates  = []

for day in percent_change_data[:-1]: 
    new_price_lev       = (1+(day['Percent Change']*3))*previous_close_lev
    new_shares          = adding_position/(float(day['Close']))
    new_shares_lev      = adding_position/new_price_lev
    total_shares        += new_shares
    total_shares_lev    += new_shares_lev
    total_position      += adding_position
    total_position_lev  += adding_position
    total_value         = total_shares * day['Close'] 
    total_value_lev     = total_shares_lev * new_price_lev
    previous_close_lev  = new_price_lev

    print("Date                 = " + day['Date'])
    print("Total Position       = " + str("{:.2f}".format(total_position)))
    print("Total Value          = " + str("{:.2f}".format(total_value)))
    print("Total Position 3x    = " + str("{:.2f}".format(total_position_lev)))
    print("Total Value 3x       = " + str("{:.2f}".format(total_value_lev)))
    print("")

    temp_dict = {}
    temp_dict['Date']           = day['Date']
    temp_dict['total value']    = total_value
    #total_value_list.append(temp_dict)
    total_value_list.append(total_value)

    temp_dict['Date']           = day['Date']
    temp_dict['total value']    = total_value_lev
    #total_value_lev_list.append(temp_dict)
    total_value_lev_list.append(total_value_lev)

    rel_total_value_list.append(total_value_lev/total_value)

    x_dates.append(day['Date'])
    
xi = list(range(len(total_value_list)))

xi2 = xi[::500]
x_dates2 = x_dates[::500]

#fig, ax = plt.subplots()

plt.plot(xi, total_value_list)
plt.plot(xi, total_value_lev_list)
plt.xticks(xi2, x_dates2)
#plt.plot(rel_total_value_list)
plt.show()

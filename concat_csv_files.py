import numpy as np
import pprint
import os
import csv
from datetime import datetime
import time
from matplotlib import pyplot as plt

from scipy.optimize import curve_fit

###########################
def getData():
  concat_csv = []

  for file in os.listdir('./qqq_data'):

    with open('./qqq_data/'+file, mode='r') as csv_file:
      csv_reader = csv.DictReader(csv_file)
      line_count = 0

      for row in csv_reader:

        if line_count == 0:
          line_count += 1

        concat_csv.append(row)
        line_count += 1
  
  sorted_data = sorted(concat_csv, key=lambda d: datetime.strptime(d['Date'], "%m/%d/%Y")) 
  return sorted_data

  #pretty_dict_str = pprint.pformat(sorted_data)
  #print(pretty_dict_str)
  
  #num_days = len(sorted_data)
  #print(num_days)
###########################


###########################
def getPercentChangeData(sorted_data):
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

  return percent_change_data
  
  #pretty_dict_str = pprint.pformat(percent_change_data)
  #print(pretty_dict_str)
###########################


###########################
def produceAddingArray(percent_change_data):
  num_days = len(percent_change_data[:-1])
  adding_array = [0]*num_days

  peak    = 1
  current = 1
  
  previous_percent_change = percent_change_data[0]['Percent Change']

  for i in range(num_days):
    current = current * (1+percent_change_data[i]['Percent Change'])
    if(current > peak):
      peak = current

    if(current < 0.50*peak):
      adding_array[i] = 100

    ##adding_array[i] = 100
    #if(previous_percent_change < 0):
    #  adding_array[i] = 200
    #else:
    #  adding_array[i] = 0
    #previous_percent_change = percent_change_data[i]['Percent Change']

  return adding_array
###########################


###########################
def computeResults(starting_position, adding_array, sorted_data, percent_change_data):
  num_days = len(percent_change_data[:-1])
  total_value_list    = []
  total_value_lev_list  = []
  rel_total_value_list  = []
  
  starting_position   = 1000.0
  
  total_position    = starting_position
  total_position_lev  = starting_position
  
  previous_close    = float(sorted_data[0]['Close'])
  previous_close_lev  = float(sorted_data[0]['Close'])
  
  total_shares    = starting_position/previous_close
  total_shares_lev  = total_shares
  
  x_dates  = []

  min_relative_value = 1.0
  max_relative_value = 1.0
  
  #for day in percent_change_data[:-1]: 
  for i in range(num_days):
    day = percent_change_data[i]
    new_price_lev       = (1+(day['Percent Change']*3))*previous_close_lev
    new_shares          = adding_array[i]/(float(day['Close']))
    new_shares_lev      = adding_array[i]/new_price_lev
    total_shares        += new_shares
    total_shares_lev    += new_shares_lev
    total_position      += adding_array[i]
    total_position_lev  += adding_array[i]
    total_value         = total_shares * day['Close'] 
    total_value_lev     = total_shares_lev * new_price_lev
    previous_close_lev  = new_price_lev

    relative_value = total_value_lev/total_value

    if(relative_value < min_relative_value):
      min_relative_value = relative_value

    if(relative_value > max_relative_value):
      max_relative_value = relative_value
  
    print("Date               = " + day['Date'])
    print("Total Position     = " + str("{:.2f}".format(total_position)))
    print("Total Value        = " + str("{:.2f}".format(total_value)))
    print("Total Position 3x  = " + str("{:.2f}".format(total_position_lev)))
    print("Total Value 3x     = " + str("{:.2f}".format(total_value_lev)))
    print("Relative Value     = " + str("{:.2f}".format(total_value_lev/total_value)))
    print("")
  
    temp_dict = {}
    temp_dict['Date']       = day['Date']
    temp_dict['total value']  = total_value
    #total_value_list.append(temp_dict)
    total_value_list.append(total_value)
  
    temp_dict['Date']       = day['Date']
    temp_dict['total value']  = total_value_lev
    #total_value_lev_list.append(temp_dict)
    total_value_lev_list.append(total_value_lev)
  
    rel_total_value_list.append(total_value_lev/total_value)
  
    x_dates.append(day['Date'])

  print("Min Relative Value = " + str("{:.2f}".format(min_relative_value)))
  print("Max Relative Value = " + str("{:.2f}".format(max_relative_value)))

  return total_value_list, total_value_lev_list, rel_total_value_list
###########################
  

###########################
def plotShit(total_value_list, total_value_lev_list, rel_total_value_list):
  xi = list(range(len(total_value_list)))
  
  #xi2 = xi[::500]
  #x_dates2 = x_dates[::500]
  
  #fig, ax = plt.subplots()
  
  plt.plot(xi, total_value_list)
  plt.plot(xi, total_value_lev_list)
  #plt.xticks(xi2, x_dates2)
  plt.yscale("log")
  
  #z  = np.polyfit(xi, total_value_list, 1)
  #z2 = np.polyfit(xi, total_value_lev_list, 1)
  
  #popt, pcov = curve_fit(lambda t, a, b, c: a*np.exp(b*t)+c, xi, total_value_list)
  
  #a = popt[0]
  #b = popt[1]
  #c = popt[2]
  
  #x_fitted = np.linspace(np.min(xi), np.max(xi), 100)
  #y_fitted = a*np.exp(b*x_fitted)+c
  
  #plt.plot(x_fitted, y_fitted)

  #p  = np.poly1d(z)
  #p2 = np.poly1d(z2)
  #
  #plt.plot(xi, p(xi))
  #plt.plot(xi, p2(xi))  
  
  #plt.plot(rel_total_value_list)
  plt.show()
###########################




sorted_data         = getData()
percent_change_data = getPercentChangeData(sorted_data)
adding_array        = produceAddingArray(percent_change_data)

starting_position   = 1000.0

total_value_list, total_value_lev_list, rel_total_value_list = computeResults(starting_position, adding_array, sorted_data, percent_change_data)

plotShit(total_value_list, total_value_lev_list, rel_total_value_list)


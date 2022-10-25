import os
import time

os.chdir('./csv')


# Takes two csv filenames, and returns a tuple whose first element is
# a list of common dates to both csv files and whose second element is
# a list containing csv1 values divided by csv2 values
def divided_dataset(csv1,csv2):
    
    startTime = time.time_ns()
    
    f1 = getFrequency(csv1)
    f2 = getFrequency(csv2)
    
    f = min(f1,f2)

    d1 = csvToList(csv1, f)
    d2 = csvToList(csv2, f)

    values = []
    dates = []
                          
    for i in d1:
        if i in d2:
            dates.append(i)
            values.append(float(d1[i])/float(d2[i]))

    timeTaken = (time.time_ns() - startTime)/1000000000
    print("time taken in seconds to produce divided data set: " + str(timeTaken))

    return (dates, values)
    #return (dates, normalize_list(values))
   
    
# Takes a string as a parameter, and returns the substring that is
# before the comma
def before_comma(string_1):
    
    return string_1[0:string_1.index(',')]
    
    
# Takes a string as a parameter, and returns the substring that is
# after the comma
def after_comma(string_1):
    
    return string_1[string_1.index(',')+1:string_1.index('\n')]    
      

# Takes a list, and returns its normalization (divided by first element)
def normalize_list(l):
    
    normalizedList = []
    startTime = time.time_ns()
    
    for i in l:
        
        normalizedList.append(i/l[0])
        
    timeTaken = (time.time_ns() - startTime)/1000000000
    print("time taken in seconds to normalize data set: " + str(timeTaken))
    
    return normalizedList


# Takes the name of a csv file as input, and returns 0, 1, 2, 3 if the 
# data is quarterly, monthly, weekly, or daily respectively
def getFrequency(csv_name):
    
    with open(csv_name, 'r') as l:
        counter = 0
        for line in l:
            if counter == 1:
                first_line = line
            last_line = line
            counter += 1
            
    lastYear = int(last_line[0:4])
    startYear = int(first_line[0:4])
    numberYears = lastYear - startYear
    
    if counter / numberYears < 5: # Quarterly
        return 0
    elif counter / numberYears < 13: # Monthly
        return 1
    elif counter / numberYears < 13: # Weekly
        return 2
    else:                           # Daily
        return 3


# Takes an integer parameter f and a string parameter line of the form
# 1962-01-02,4.06
# Returns True if the date in the line is of the wanted frequency f.
def dateChecker(f, line):
    
    if f == 1:
        return line[8:10] == "01"
    elif f == 2:
        return int(line[8:10]) <= 7
    elif f == 3:
        return int(line[8:10]) <= 4 or int(line[8:10]) >= 26
    else:
        return  ((int(line[5:7])+2)%3 == 0) and  line[8:10] == "01"
        
        
# Takes the name of a csv file, and returns a list containing its lines
# Removes the first line from the csv
def csvToList(csv_name, f):

    returnedDict = {}
    startTime = time.time_ns()

    with open(csv_name, 'r') as infile:

        counter = 0

        for line in infile:
            after = after_comma(line)

            if counter != 0  and after != "." and dateChecker(f, line):
                returnedDict[before_comma(line)] = after

            counter += 1

    timeTaken = (time.time_ns() - startTime)/1000000000
    print("time taken in seconds to convert csv to dictionary: " + str(timeTaken))
     
    return returnedDict

from courseInfoGrab import *
from getInfo import *
from visualTable import *
from tabulate import tabulate
from itertools import product
import sys

DEBUG = 0
USER = 0
VIS = 1
# have to be 3 letters + 3 int + 's' or 'f' or 'y'

if USER:
    while True:
        courses = []
        num = input('Hi, there! \nThis is an simple class timetable schedule made by Rico Qian. \nPlease input the number of courses you want to choose: \n')
        
        while True:
            num = num.strip()
            if num and num.isdigit() and 0<int(num)<14:
                break
            num = input('Sorry, your input \'{}\' is incorrect. Please input a positive integer within 14: \n'.format(num))
        i = 0
        error = 0
        while i < int(num):
            if i > 0 and not error:
                s = 'Your last course code is: ' + str(c) + '\n'
            elif not error:
                s = 'Thank you. Your input number is ' + str(num) + '\n'
            
            c = input(s + 'Please input the course code \n(3 letters + 3 int + \'s\' or \'f\' or \'y\'. e.g.: csc384f). \nPress return for each course: \n')
            c = c.strip()
            if c in courses:
                error = 1
                s = 'Sorry, your course code \'{}\' is already exist.\n'.format(c)
            elif len(c)==7 and c[:3].isalpha() and c[3:6].isdigit() and c[-1] in ['s', 'y', 'f']:            
                i += 1
                error = 0
                courses.append(c)
            else:
                error = 1
                s = 'Sorry, your course code \'{}\' format is incorrect \n'
                
            print('\ncourses input: {}/{}'.format(i,num))
    
        print('\nWaiting for the result...  :)\n')
else:
    courses = ['mat235y', "imc200f", 'csc418s', 'Csc324f', 'csc488s', 'csc420f', 'APM236s', 'env200s', 'csc384F', 'csc486s'] 
    # prase course information
    info = courseinfoGrab(courses, DEBUG)
    if type(info)==str:
        print('Sorry! There is no {} in {} term.'.format(info[:-1].upper(), info[-1].upper()))
    else:
        
        # get useful part of information from info
        classes = getInfo(courses, info)
        
        # get scheduling
        result = classScheduling(classes)
        
        # visualize result in fall and winter timetable
        if VIS:
            headers, tables, btm = visualTable(result, classes)     
            print('Fall Timetable:\n')
            print(tabulate(tables[0], headers[0], tablefmt="fancy_grid"))
            print('Winter Timetable:\n')
            print(tabulate(tables[1], headers[1], tablefmt="fancy_grid"))        
            print(btm)
    sys.exit('Finished! \nThanks for using my class timetable schedule program! \nHave a Nice day!\n')

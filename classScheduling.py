from courseInfo_grabber import *
from infoForClassSched import *
from tabulate import tabulate
from itertools import product
import sys

DEBUG = 0

# have to be 3 letters + 3 int + 's' or 'f' or 'y'
# courses = ['mat235y', "imc200f", 'csc418s', 'Csc324f', 'csc488s', 'csc420f', 'APM236s', 'env200s', 'csc384F', 'csc486s', 'sta248s'] 
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
    
    # prase course information
    info = courseinfo_grab(courses, DEBUG)
    if type(info)==str:
        b = input('Sorry! There is no {} in {} term. Do you want to try again? (y/n)\n'.format(info[:-1].upper(), info[-1].upper()))
        if b.startswith('n'):
            sys.exit('Thank you! Have a Nice day!\n')
        else:
            pass
    else:
        
        # get useful part of information from info
        classes = getInfo(courses, info)
        
        # get scheduling
        result = classScheduling(classes)
        
        # visualize result in fall and winter timetable
        tables = [[], []]
        headers = []
        headers.append(['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        headers.append(['Time', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'])
        btm = ''
        for course in result:
            terms = []
            if course[-4] in ['Y','F']:
                terms.append(0)
            if course[-4] in ['Y', 'S']:
                terms.append(1)
            for c in classes:
                if c.name.startswith(course[:6]) and c.tp==course[-2]:
                    
                    if not c.classTimes[result[course]]:
                        btm = btm + course + ' is an ONLINE course.\n'
                        break
                    
                    for t in c.classTimes[result[course]]:
                        table = [''] *(len(headers[0])-1)
                        if t.weekday == 'M':
                            table[0] = course
                        elif t.weekday == 'T':
                            table[1] = course
                        elif t.weekday == 'W':
                            table[2] = course
                        elif t.weekday == 'R':
                            table[3] = course
                        elif t.weekday == 'F':
                            table[4] = course

                        Tt = range(t.startTime, t.finishTime)
                        for T in Tt:
                            T = str(T)
                            if len(T)==1:
                                T = '0' + T
                            exist=0
                            for term in terms:
                                for L in tables[term]:
                                    if L[0] == T:
                                        exist=1
                                        for i in range(len(table)):
                                            if table[i]:
                                                L[i+1] = table[i]
                                if not exist:
                                    tables[term].append([T]+table)
                    break
                
                
        tables[0] = sorted(tables[0])
        tables[1] = sorted(tables[1])
        print('Fall Timetable:\n')
        print(tabulate(tables[0], headers[0], tablefmt="fancy_grid"))
        print('Winter Timetable:\n')
        print(tabulate(tables[1], headers[1], tablefmt="fancy_grid"))
        print(btm)

        sys.exit('Finished! \nThanks for using my class timetable schedule program! \nHave a Nice day!\n')
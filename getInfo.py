from classTime import *


def getInfo(courses, info):
    classes = []
    for course in courses:
        name = course[:-1]
        term = ''
        tp = ''
        i = 0
        restrict_class = 0
        while i < len(info[course]):
            session = info[course][i]
            
            if not '\xa0' in session[0]:
                term = session[0]
                tp = session[2][0]
                code = session[2]
                c = Class(name, term, tp, [code])
                classes.append(c)
                restrict_class = 0
                
            elif not '\xa0' in session[2] and not session[2].startswith('L2'):
                code = session[2]
                if tp.upper() == 'L' and session[2][0].upper() == 'T':
                    tp = session[2][0]
                    c = Class(name, term, tp)
                    classes.append(c)
                c.addSession(code)
                code = session[2]
                restrict_class = 0
            elif session[2].startswith('L2'):
                restrict_class = 1
            if not restrict_class:
                times = getTime(session[4])
                for t in times:
                    c.addTime(code, t)
            i += 1
    return classes

def getTime(s):
    startTime = 0
    finishTime = 0
    weekdays = []
    ind = s.find('-')
    pi = s.find('(')
    if pi != -1:
        s = s[:pi]
    if ind == -1:
        ind = len(s)
    if s.isalpha(): # Online course
        return []
    for i in range(len(s[:ind])):
        if s[i].isalpha():
            weekdays.append(s[i])
        elif s[i].isdigit():
            startTime = int(s[i:ind])
            if startTime < 8:
                startTime += 12
            break
    if ind != len(s):
        finishTime = int(s[ind+1:])
        if finishTime < 10:
            finishTime += 12
    if startTime==0:
        raise Exception('No start time found!')
    result = []
    for weekday in weekdays:
        result.append(classTime(weekday, startTime, finishTime))

    return result

from cspbase import *
from propagators import *

# Class for course
class Class:
    # name -> string, sessions -> [string], tp = 'l' or 't', classTimeList -> {string: [classTime]}
    def __init__(self, name, term, tp, sessions=[]):
        self.name = name.upper()
        self.term = term.upper()
        self.tp = tp.upper()
        self.classTimes = {}
        for s in sessions:
            self.classTimes[s.upper()] = []
    
    def addSession(self, session):
        if session in self.classTimes:
            print(str(session) + ' already exists!')
        else:
            self.classTimes[session.upper()] = []
    
    def addTime(self, s, classTime):
        if classTime in self.classTimes[s]:
            print(str(self) + ' ' + str(classTime) + ' already exists!')
        else:
            classTime.term = self.term
            self.classTimes[s].append(classTime)
        
    def __str__(self):
        return self.name + self.tp + '( ' + self.term + ' ): ' + str(self.classTimes)
    
# return non overlap sessions of two courses, [] if there are always conflict
def notOverlap(self, other):
    result = []
    for s1 in self.classTimes:
        for s2 in other.classTimes:
            if not sessionOverlap(self.classTimes[s1], other.classTimes[s2]):
                result.append([s1, s2])
    return result

# check if two sessions are overlap
def sessionOverlap(s1, s2):
    for t1 in s1:
        for t2 in s2:
            if isOverlap(t1, t2):
                return True
    return False

# excute prop_GAC and get the result
def classScheduling(classes):
    allclasses = []
    for c in classes:
        session_list = []
        for s in c.classTimes:
            session_list.append(s)
        allclasses.append(Variable('{}{}({})'.format(c.name,c.term,c.tp), session_list))
    
    
    cons = []
    for qi in range(len(allclasses)):
        for qj in range(qi+1, len(allclasses)):
            con = Constraint("C(Q{},Q{})".format(qi+1,qj+1), [allclasses[qi], allclasses[qj]])
            sat_tuples = notOverlap(classes[qi], classes[qj])
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)
        
    csp = CSP("schedule", allclasses)
    
    for cc in cons:
        csp.add_constraint(cc)
    solver = BT(csp)
    #solver.trace_on()
    return solver.bt_search(prop_GAC)

# one time slot
class classTime:
    # weekday = 'M' or 'T' or 'W' or 'R' or 'F', term = 'S' or 'F' or 'Y', startTime, finishTime -> 0 < x < 24
    def __init__(self, weekday, startTime, finishTime=0):
        self.weekday = weekday.upper()
        self.startTime = startTime
        if finishTime:
            self.finishTime = finishTime
        else:
            self.finishTime = startTime+1
        self.term = None
    
    def __eq__(self, other):
        return self.weekday == other.weekday and \
               self.startTime == other.startTime and \
               self.finishTime == other.finishTime
    
    def __str__(self):
        return 'Start from {} to {} in {}.'.format(self.startTime, self.finishTime, self.weekday)
    
    def __repr__(self):
        return 'classTime({}, {}, {})'.format(self.weekday, self.startTime, self.finishTime)
    
# check if two time slots (classTime) are overlap each other
def isOverlap(self, other):
    return (self.term == other.term or self.term == 'Y' or other.term == 'Y') and self.weekday == other.weekday and ( \
        (self.startTime > other.startTime and self.startTime < other.finishTime) or \
        (self.startTime < other.startTime and self.finishTime > other.startTime) )


import urllib.request
from bs4 import BeautifulSoup

# parser return a dictionary info[course] = list of course information i.e. 
# [course_name, term, title, session, waitinglist, time, etc.] only need 
# course_name, term, session and time for this program
def courseinfo_grab(courses, debug=0):
    def Print(s):
        if debug:
            print(s)
    
    def isValidName(course):
        return course[:3].isalpha() and course[3:6].isdigit() and \
               (course.lower().endswith('f') or course.lower().endswith('s') or course.lower().endswith('y')) \
               and len(course)==7    
    
    info = {}
    for course in courses:
        if not isValidName(course):
            Print(course)
            raise Exception('not valid name, please input 3 letters + 3 digits + f or s')
        info[course] = []
    
    for course in courses:
        wp = urllib.request.urlopen("http://www.artsandscience.utoronto.ca/ofr/timetable/winter/")
        soup = BeautifulSoup(wp, "html.parser")
        links = []
        for l in soup.find_all('a'):
            if course[:3].upper() in l.string:
                link = l.get('href')
                links.append(link)
                Print(l.string)
                Print(link)
        i = 0        
        while not info[course] and i<len(links):
            link = links[i]
            wp = urllib.request.urlopen("http://www.artsandscience.utoronto.ca/ofr/timetable/winter/"+link)
            soup = BeautifulSoup(wp, "html.parser")
            find = 0
            for tr in soup.find_all('tr'):
                a = tr.a
                Print(a)
                if find==0 and a and a.string.upper().startswith(course[:6].upper()):
                    session = []
                    for td in tr.findAll('td'):
                        Print(td.string)
                        session.append(td.string)
                    if course[-1].upper() in session:
                        info[course].append(session[1:])
                        find = 1
                
                elif find==1 and (not a or len(a.string)!=8):
                    session = []
                    for td in tr.findAll('td'):
                        session.append(td.string)
                    if len(session) > 12:
                        info[course].append(session[1:])
                elif find==1 and a and len(a.string)==8:
                    Print(a.string)
                    break
            i += 1
        if not info[course]:
            return course
    for course in info:
        Print(course+': ')
        for data in info[course]:
            Print(str(data))
    
    return info
def visualTable(result, classes):
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
    return headers, tables, btm
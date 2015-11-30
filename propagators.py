def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    result_list = set()
    GAC_Q = []
    if not newVar:
        for c in csp.get_all_cons():
            GAC_Q.append(c)
        while GAC_Q != []:
            again = [0, set()]
            c = GAC_Q[0]
            del GAC_Q[0]
            uv_l = c.get_unasgn_vars()
            for uv in uv_l:
                right = 0
                vals_uv = uv.cur_domain()
                for val_uv in vals_uv:
                    if not c.has_support(uv, val_uv):
                        uv.prune_value(val_uv)
                        result_list.add((uv, val_uv))
                        again[0] = 1
                        again[1].add(uv)
                    else:
                        right += 1
                if right == 0:
                    return False, list(result_list)
            if again[0] == 1:
                for c2 in csp.get_all_cons():
                    if not c2 in GAC_Q and any([x in c2.get_scope() for x in again[1]]):
                        GAC_Q.append(c2)
    else:
        for c in csp.get_cons_with_var(newVar):
            GAC_Q.append(c)
        while GAC_Q != []:
            again = [0, set()]
            c = GAC_Q[0]
            del GAC_Q[0]
            uv_l = c.get_unasgn_vars()
            for uv in uv_l:
                right = 0
                vals_uv = uv.cur_domain()
                for val_uv in vals_uv:
                    if not c.has_support(uv, val_uv):
                        uv.prune_value(val_uv)
                        result_list.add((uv, val_uv))
                        again[0] = 1
                        again[1].add(uv)
                    else:
                        right += 1
                if right == 0:
                    return False, list(result_list)
            if again[0] == 1:
                for c2 in csp.get_all_cons():
                    if not c2 in GAC_Q and any([x in c2.get_scope() for x in again[1]]):
                        GAC_Q.append(c2)
    return True, list(result_list)

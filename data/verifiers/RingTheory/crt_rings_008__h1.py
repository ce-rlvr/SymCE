import itertools

# Top-level setup
S3 = None
Z2 = None
Z3 = None
Z4 = None

def conditions(witness):
    try:
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'ideals'):
            raw_elements = witness.elements
            elem_to_idx = {e: i for i, e in enumerate(raw_elements)}
            n_elements = len(raw_elements)
            R_add = [[elem_to_idx[witness.add(x, y)] for y in raw_elements] for x in raw_elements]
            R_mul = [[elem_to_idx[witness.mul(x, y)] for y in raw_elements] for x in raw_elements]
            I_list = [[elem_to_idx[x] for x in I] for I in witness.ideals]
            elements = list(range(n_elements))
        elif isinstance(witness, tuple) and len(witness) == 3:
            R_add, R_mul, I_list = witness
            n_elements = len(R_add)
            elements = list(range(n_elements))
        else:
            return [False, False, False]
            
        zero = None
        for e in elements:
            if all(R_add[e][x] == x for x in elements):
                zero = e
                break
        if zero is None:
            return [False, False, False]
            
        neg = [0] * n_elements
        for x in elements:
            for y in elements:
                if R_add[x][y] == zero:
                    neg[x] = y
                    break
                    
        h1 = True
        for I in I_list:
            if not I:
                h1 = False
                break
            for x in I:
                for y in I:
                    if R_add[x][y] not in I:
                        h1 = False
            for x in I:
                for r in elements:
                    if R_mul[r][x] not in I or R_mul[x][r] not in I:
                        h1 = False
                        
        h2 = True
        n = len(I_list)
        for i in range(n):
            for j in range(i + 1, n):
                sum_ideal = set()
                for x in I_list[i]:
                    for y in I_list[j]:
                        sum_ideal.add(R_add[x][y])
                if len(sum_ideal) != n_elements:
                    h2 = False
                    
        if n == 0:
            intersect = elements
        else:
            intersect = [x for x in elements if all(x in I for I in I_list)]
            
        def get_unit_group(I):
            cosets = []
            for x in elements:
                found = False
                for c in cosets:
                    if R_add[x][neg[c[0]]] in I:
                        c.append(x)
                        found = True
                        break
                if not found:
                    cosets.append([x])
            
            q_elements = list(range(len(cosets)))
            q_mul = [[0]*len(cosets) for _ in range(len(cosets))]
            for i in q_elements:
                for j in q_elements:
                    prod = R_mul[cosets[i][0]][cosets[j][0]]
                    for k in q_elements:
                        if R_add[prod][neg[cosets[k][0]]] in I:
                            q_mul[i][j] = k
                            break
                            
            q_id = None
            for e in q_elements:
                if all(q_mul[e][x] == x and q_mul[x][e] == x for x in q_elements):
                    q_id = e
                    break
            if q_id is None:
                return None
                
            units = []
            for u in q_elements:
                for v in q_elements:
                    if q_mul[u][v] == q_id and q_mul[v][u] == q_id:
                        units.append(u)
                        break
            
            unit_idx = {u: i for i, u in enumerate(units)}
            table = []
            for u in units:
                row = []
                for v in units:
                    uv = q_mul[u][v]
                    if uv in unit_idx:
                        row.append(unit_idx[uv])
                    else:
                        return None
                table.append(row)
            return table

        def are_isomorphic(t1, t2):
            if t1 is None or t2 is None:
                return False
            if len(t1) != len(t2):
                return False
            n_t = len(t1)
            if n_t == 0:
                return True
            
            id1 = next(i for i in range(n_t) if all(t1[i][j] == j for j in range(n_t)))
            id2 = next(i for i in range(n_t) if all(t2[i][j] == j for j in range(n_t)))
            
            def get_orders(t, id_elem):
                orders = []
                for i in range(n_t):
                    curr = i
                    order = 1
                    while curr != id_elem:
                        curr = t[curr][i]
                        order += 1
                        if order > n_t:
                            break
                    orders.append(order)
                return orders
                
            orders1 = get_orders(t1, id1)
            orders2 = get_orders(t2, id2)
            
            if sorted(orders1) != sorted(orders2):
                return False
                
            cands = []
            for i in range(n_t):
                cands.append([j for j in range(n_t) if orders2[j] == orders1[i]])
                
            for p in itertools.product(*cands):
                if len(set(p)) != n_t:
                    continue
                if p[id1] != id2:
                    continue
                iso = True
                for i in range(n_t):
                    for j in range(n_t):
                        if p[t1[i][j]] != t2[p[i]][p[j]]:
                            iso = False
                            break
                    if not iso:
                        break
                if iso:
                    return True
            return False

        def direct_product(tables):
            if not tables:
                return [[0]]
            res = tables[0]
            for t in tables[1:]:
                if res is None or t is None:
                    return None
                n1 = len(res)
                n2 = len(t)
                new_res = [[0]*(n1*n2) for _ in range(n1*n2)]
                for i1 in range(n1):
                    for i2 in range(n2):
                        for j1 in range(n1):
                            for j2 in range(n2):
                                new_res[i1*n2 + i2][j1*n2 + j2] = res[i1][j1]*n2 + t[i2][j2]
                res = new_res
            return res

        lhs_table = get_unit_group(intersect)
        rhs_tables = [get_unit_group(I) for I in I_list]
        
        if any(t is None for t in rhs_tables) or lhs_table is None:
            neg_q = True
        else:
            rhs_table = direct_product(rhs_tables)
            neg_q = not are_isomorphic(lhs_table, rhs_table)
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I_1, ..., I_n are ideals of R",
    "H_2: I_i + I_j = R for all i != j",
    "¬Q: The group of units (R/\\cap I_k)^x is NOT isomorphic to \\prod (R/I_k)^x"
]

N_HYP = 2
NEG_Q_INDEX = 2
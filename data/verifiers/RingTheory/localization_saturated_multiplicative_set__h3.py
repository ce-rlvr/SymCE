import sympy
from sympy import ZZ, QQ

# Top-level setup
# (No specific named rings required beyond ZZ and QQ, which are imported)

def conditions(witness):
    try:
        # Try to parse as (n, S) representing Z/nZ and a subset S
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, S_obj = witness
            
            if isinstance(R_obj, int):
                n = R_obj
                S = list(set(S_obj))
                
                h1 = (n >= 1)
                
                h2 = True
                for x in S:
                    if not (isinstance(x, int) and 0 <= x < n):
                        h2 = False
                        break
                if h2:
                    for x in S:
                        for y in S:
                            if (x * y) % n not in S:
                                h2 = False
                                break
                        if not h2:
                            break
                            
                elements = list(range(n))
                add_func = lambda a, b: (a + b) % n
                mul_func = lambda a, b: (a * b) % n
                zero = 0
                
                if not S:
                    neg_q = True
                else:
                    def neg(b):
                        return (n - b) % n
                        
                    def get_classes(S_set):
                        classes = []
                        for r in elements:
                            for s in S_set:
                                p = (r, s)
                                found = False
                                for c in classes:
                                    r1, s1 = p
                                    r2, s2 = c[0]
                                    term1 = mul_func(r1, s2)
                                    term2 = mul_func(r2, s1)
                                    diff = add_func(term1, neg(term2))
                                    eq_holds = False
                                    for t in S_set:
                                        if mul_func(t, diff) == zero:
                                            eq_holds = True
                                            break
                                    if eq_holds:
                                        c.append(p)
                                        found = True
                                        break
                                if not found:
                                    classes.append([p])
                        return classes

                    classes_S = get_classes(S)
                    
                    S_bar = []
                    for x in elements:
                        for y in elements:
                            if mul_func(x, y) in S:
                                S_bar.append(x)
                                break
                                
                    if not S_bar:
                        neg_q = True
                    else:
                        classes_S_bar = get_classes(S_bar)
                        neg_q = (len(classes_S) != len(classes_S_bar))
                        
                return [bool(h1), bool(h2), bool(neg_q)]
                
            elif hasattr(R_obj, 'is_ring') and R_obj.is_ring:
                # Sympy ring
                h1 = bool(R_obj.is_commutative)
                
                S = list(S_obj)
                h2 = True
                for x in S:
                    if x not in R_obj:
                        h2 = False
                        break
                if h2:
                    for x in S:
                        for y in S:
                            if (x * y) not in S:
                                h2 = False
                                break
                                
                # If S is empty, S^{-1}R is not a ring, so they are not isomorphic rings.
                # If S is non-empty, they are always canonically isomorphic.
                neg_q = (len(S) == 0)
                return [bool(h1), bool(h2), bool(neg_q)]
                
        # Try to parse as (add_table, mul_table, S) representing an arbitrary finite ring
        elif isinstance(witness, tuple) and len(witness) == 3:
            add_table, mul_table, S = witness
            n = len(add_table)
            elements = list(range(n))
            
            h1 = True
            for i in range(n):
                for j in range(n):
                    if mul_table[i][j] != mul_table[j][i]:
                        h1 = False
                    if add_table[i][j] != add_table[j][i]:
                        h1 = False
                    for k in range(n):
                        if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                            h1 = False
                        if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                            h1 = False
                        if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                            h1 = False
                        if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                            h1 = False
                            
            zero = None
            for i in range(n):
                if all(add_table[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero is None:
                h1 = False
                zero = 0
                
            for i in range(n):
                has_inv = False
                for j in range(n):
                    if add_table[i][j] == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
            
            h2 = True
            for x in S:
                if not (isinstance(x, int) and 0 <= x < n):
                    h2 = False
                    break
            if h2:
                for x in S:
                    for y in S:
                        if mul_table[x][y] not in S:
                            h2 = False
                            break
                            
            if not S:
                neg_q = True
            else:
                def neg(b):
                    for x in elements:
                        if add_table[b][x] == zero:
                            return x
                    return b
                    
                def get_classes(S_set):
                    classes = []
                    for r in elements:
                        for s in S_set:
                            p = (r, s)
                            found = False
                            for c in classes:
                                r1, s1 = p
                                r2, s2 = c[0]
                                term1 = mul_table[r1][s2]
                                term2 = mul_table[r2][s1]
                                diff = add_table[term1][neg(term2)]
                                eq_holds = False
                                for t in S_set:
                                    if mul_table[t][diff] == zero:
                                        eq_holds = True
                                        break
                                if eq_holds:
                                    c.append(p)
                                    found = True
                                    break
                            if not found:
                                classes.append([p])
                    return classes

                classes_S = get_classes(S)
                
                S_bar = []
                for x in elements:
                    for y in elements:
                        if mul_table[x][y] in S:
                            S_bar.append(x)
                            break
                            
                if not S_bar:
                    neg_q = True
                else:
                    classes_S_bar = get_classes(S_bar)
                    neg_q = (len(classes_S) != len(classes_S_bar))
                    
            return [bool(h1), bool(h2), bool(neg_q)]
            
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The localized rings S^{-1}R and \\bar{S}^{-1}R are NOT canonically isomorphic"
]

N_HYP = 2
NEG_Q_INDEX = 2
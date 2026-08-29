import sympy
from sympy import Matrix

# Top-level setup for standard rings
Z2 = list(range(2))
Z3 = list(range(3))
Z4 = list(range(4))
Z5 = list(range(5))
Z6 = list(range(6))
ZZ = sympy.ZZ
QQ = sympy.QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be provided in two formats:
      1. (R, I, J) where R is a standard ring (e.g., ZZ, Z4) and I, J are subsets.
      2. (R_add, R_mul, I, J) where R_add and R_mul are n x n Cayley tables for the ring.
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if len(witness) == 4:
            R_add, R_mul, I, J = witness
            
            # H1: R is a ring
            try:
                n = len(R_add)
                if len(R_mul) == n and all(len(row) == n for row in R_add) and all(len(row) == n for row in R_mul):
                    if not any(val < 0 or val >= n for row in R_add for val in row) and \
                       not any(val < 0 or val >= n for row in R_mul for val in row):
                        # Commutativity of addition
                        if all(R_add[i][j] == R_add[j][i] for i in range(n) for j in range(n)):
                            # Associativity of addition
                            if all(R_add[R_add[i][j]][k] == R_add[i][R_add[j][k]] for i in range(n) for j in range(n) for k in range(n)):
                                # Additive identity
                                e = -1
                                for i in range(n):
                                    if all(R_add[i][j] == j for j in range(n)):
                                        e = i
                                        break
                                if e != -1:
                                    # Additive inverses
                                    if all(any(R_add[i][j] == e for j in range(n)) for i in range(n)):
                                        # Associativity of multiplication
                                        if all(R_mul[R_mul[i][j]][k] == R_mul[i][R_mul[j][k]] for i in range(n) for j in range(n) for k in range(n)):
                                            # Distributivity
                                            if all(R_mul[i][R_add[j][k]] == R_add[R_mul[i][j]][R_mul[i][k]] for i in range(n) for j in range(n) for k in range(n)) and \
                                               all(R_mul[R_add[i][j]][k] == R_add[R_mul[i][k]][R_mul[j][k]] for i in range(n) for j in range(n) for k in range(n)):
                                                h1 = True
            except Exception:
                h1 = False
                
            # H2: I subseteq J
            try:
                h2 = all(x in J for x in I)
            except Exception:
                h2 = False
                
            # neg_Q: The conclusion fails if I or J is not an ideal of R
            try:
                def is_ideal_cayley(S):
                    if not S: return False
                    if not isinstance(S, (list, set, tuple)): return False
                    if any(x < 0 or x >= n for x in S): return False
                    
                    # Additive closure
                    if any(R_add[a][b] not in S for a in S for b in S): return False
                    
                    # Additive inverse
                    e = -1
                    for i in range(n):
                        if all(R_add[i][j] == j for j in range(n)):
                            e = i
                            break
                    for a in S:
                        inv_a = -1
                        for b in range(n):
                            if R_add[a][b] == e:
                                inv_a = b
                                break
                        if inv_a not in S: return False
                        
                    # Multiplicative absorption
                    if any(R_mul[r][s] not in S for r in range(n) for s in S): return False
                    if any(R_mul[s][r] not in S for r in range(n) for s in S): return False
                    
                    return True
                
                neg_q = not (is_ideal_cayley(I) and is_ideal_cayley(J))
            except Exception:
                neg_q = False

        elif len(witness) == 3:
            R, I, J = witness
            
            # H1: R is a ring
            try:
                if R in (sympy.ZZ, sympy.QQ):
                    h1 = True
                elif isinstance(R, (list, set, tuple)):
                    R_list = list(R)
                    if not R_list:
                        h1 = False
                    elif all(isinstance(x, int) for x in R_list):
                        if set(R_list) == set(range(len(R_list))):
                            h1 = True
                    elif all(isinstance(x, sympy.Matrix) for x in R_list):
                        h1 = True
                        for a in R_list:
                            for b in R_list:
                                if (a + b) not in R_list: h1 = False
                                if (a * b) not in R_list: h1 = False
                        if h1:
                            zero = R_list[0] - R_list[0]
                            if zero not in R_list:
                                h1 = False
                            else:
                                for a in R_list:
                                    if (-a) not in R_list:
                                        h1 = False
            except Exception:
                h1 = False
                
            # H2: I subseteq J
            try:
                h2 = all(x in J for x in I)
            except Exception:
                h2 = False
                
            # neg_Q: The conclusion fails if I or J is not an ideal of R
            try:
                def is_ideal_set(S):
                    if not S: return False
                    if not isinstance(S, (list, set, tuple)): return False
                    
                    if R in (sympy.ZZ, sympy.QQ):
                        return set(S) == {0}
                    
                    S_list = list(S)
                    R_list = list(R)
                    
                    for s in S_list:
                        if s not in R_list: return False
                        
                    if all(isinstance(x, int) for x in R_list):
                        n = len(R_list)
                        add = lambda a, b: (a + b) % n
                        mul = lambda a, b: (a * b) % n
                        inv = lambda a: (-a) % n
                    elif all(isinstance(x, sympy.Matrix) for x in R_list):
                        add = lambda a, b: a + b
                        mul = lambda a, b: a * b
                        inv = lambda a: -a
                    else:
                        return False
                        
                    # Additive closure and inverses
                    for a in S_list:
                        for b in S_list:
                            if add(a, b) not in S_list: return False
                        if inv(a) not in S_list: return False
                        
                    # Multiplicative absorption
                    for s in S_list:
                        for r in R_list:
                            if mul(r, s) not in S_list: return False
                            if mul(s, r) not in S_list: return False
                    return True
                
                neg_q = not (is_ideal_set(I) and is_ideal_set(J))
            except Exception:
                neg_q = False
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is a subset of J",
    "¬Q: J/I is not an ideal of R/I, or the quotient ring (R/I)/(J/I) is not isomorphic to R/J"
]

N_HYP = 2
NEG_Q_INDEX = 2
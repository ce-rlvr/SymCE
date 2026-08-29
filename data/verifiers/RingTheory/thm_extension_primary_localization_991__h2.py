import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Q is a P-primary ideal in R",
    "¬Q: The extended ideal Q R_P is not a P R_P-primary ideal in the localization R_P"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_commutative_ring(n, add, mul):
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            if mul[i][j] != mul[j][i]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
    one = -1
    for i in range(n):
        if all(mul[i][j] == j for j in range(n)):
            one = i
            break
    if one == -1: return False
    return True

def is_ideal(n, add, mul, I):
    if not I: return False
    I_set = set(I)
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero not in I_set: return False
    for x in I_set:
        for y in I_set:
            if add[x][y] not in I_set: return False
    for x in I_set:
        for r in range(n):
            if mul[x][r] not in I_set: return False
    return True

def radical(n, mul, I):
    I_set = set(I)
    rad = set()
    for x in range(n):
        curr = x
        for _ in range(n):
            if curr in I_set:
                rad.add(x)
                break
            curr = mul[curr][x]
    return rad

def is_primary(n, add, mul, Q, P):
    Q_set = set(Q)
    P_set = set(P)
    if not is_ideal(n, add, mul, Q): return False
    if not is_ideal(n, add, mul, P): return False
    if len(Q_set) == n: return False 
    rad_Q = radical(n, mul, Q)
    if rad_Q != P_set: return False
    
    for x in range(n):
        for y in range(n):
            if mul[x][y] in Q_set:
                if x not in Q_set and y not in rad_Q:
                    return False
    return True

def localization(n, add, mul, P):
    S = [x for x in range(n) if x not in P]
    if not S: return None
    
    S_closure = set(S)
    added = True
    while added:
        added = False
        new_elements = set()
        for s1 in S_closure:
            for s2 in S_closure:
                prod = mul[s1][s2]
                if prod not in S_closure:
                    new_elements.add(prod)
        if new_elements:
            S_closure.update(new_elements)
            added = True
    S_list = list(S_closure)
    
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
            
    def neg(x):
        for i in range(n):
            if add[x][i] == zero:
                return i
        return zero

    classes = []
    for a in range(n):
        for s in S_list:
            found = False
            for cls in classes:
                b, t = cls[0]
                equiv = False
                for u in S_list:
                    at = mul[a][t]
                    bs = mul[b][s]
                    diff = add[at][neg(bs)]
                    if mul[u][diff] == zero:
                        equiv = True
                        break
                if equiv:
                    cls.append((a, s))
                    found = True
                    break
            if not found:
                classes.append([(a, s)])
                
    m = len(classes)
    RP_add = [[0]*m for _ in range(m)]
    RP_mul = [[0]*m for _ in range(m)]
    
    for i in range(m):
        a, s = classes[i][0]
        for j in range(m):
            b, t = classes[j][0]
            at = mul[a][t]
            bs = mul[b][s]
            num_add = add[at][bs]
            den_add = mul[s][t]
            for k in range(m):
                if (num_add, den_add) in classes[k]:
                    RP_add[i][j] = k
                    break
            
            num_mul = mul[a][b]
            den_mul = mul[s][t]
            for k in range(m):
                if (num_mul, den_mul) in classes[k]:
                    RP_mul[i][j] = k
                    break
                    
    return m, RP_add, RP_mul, classes

def extended_ideal(n, add, mul, classes, I):
    m = len(classes)
    I_RP = set()
    for i in range(m):
        for (a, s) in classes[i]:
            if a in I:
                I_RP.add(i)
                break
    return list(I_RP)

def check_neg_Q(n, add, mul, Q, P):
    res = localization(n, add, mul, P)
    if res is None: return False
    m, RP_add, RP_mul, classes = res
    Q_RP = extended_ideal(n, add, mul, classes, Q)
    P_RP = extended_ideal(n, add, mul, classes, P)
    
    is_prim = is_primary(m, RP_add, RP_mul, Q_RP, P_RP)
    return not is_prim

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            n, Q_gens, P_gens = witness
            if isinstance(n, int) and isinstance(Q_gens, list) and isinstance(P_gens, list):
                add = [[(i + j) % n for j in range(n)] for i in range(n)]
                mul = [[(i * j) % n for j in range(n)] for i in range(n)]
                
                def get_ideal(gens):
                    I = set([0])
                    for g in gens:
                        new_I = set(I)
                        for r in range(n):
                            new_I.add((r * g) % n)
                        I.update(new_I)
                    added = True
                    while added:
                        added = False
                        new_I = set(I)
                        for x in I:
                            for y in I:
                                if (x + y) % n not in new_I:
                                    new_I.add((x + y) % n)
                                    added = True
                        I = new_I
                    return list(I)
                    
                Q = get_ideal(Q_gens)
                P = get_ideal(P_gens)
                
                h1 = is_commutative_ring(n, add, mul)
                h2 = is_primary(n, add, mul, Q, P)
                neg_q = check_neg_Q(n, add, mul, Q, P)
                return [h1, h2, neg_q]
                
        if isinstance(witness, tuple) and len(witness) == 5:
            n, add, mul, Q, P = witness
            if isinstance(n, int) and isinstance(add, list) and isinstance(mul, list):
                h1 = is_commutative_ring(n, add, mul)
                h2 = is_primary(n, add, mul, Q, P)
                neg_q = check_neg_Q(n, add, mul, Q, P)
                return [h1, h2, neg_q]
    except Exception:
        pass
    return [False, False, False]
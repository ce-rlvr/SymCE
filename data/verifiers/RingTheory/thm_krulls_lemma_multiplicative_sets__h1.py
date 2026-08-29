import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

def is_ring(n, add, mul):
    if not isinstance(n, int) or n <= 0: return False
    if len(add) != n or any(len(row) != n for row in add): return False
    if len(mul) != n or any(len(row) != n for row in mul): return False
    
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
            if add[i][j] != add[j][i]: return False
            
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
        
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                
    return True

def is_ideal(n, add, mul, zero, I):
    if not I: return False
    I_set = set(I)
    for x in I_set:
        for y in I_set:
            if add[x][y] not in I_set: return False
    for x in I_set:
        for r in range(n):
            if mul[r][x] not in I_set: return False
            if mul[x][r] not in I_set: return False
    return True

def is_multiplicative_subset(n, mul, S):
    if not S: return False
    S_set = set(S)
    for x in S_set:
        for y in S_set:
            if mul[x][y] not in S_set: return False
    return True

def is_maximal_disjoint_ideal(n, add, mul, zero, S, I):
    if not is_ideal(n, add, mul, zero, I): return False
    S_set = set(S)
    I_set = set(I)
    if not S_set.isdisjoint(I_set): return False
    
    for x in range(n):
        if x in I_set: continue
        J = set(I_set)
        J.add(x)
        changed = True
        while changed:
            changed = False
            new_elements = set()
            for a in J:
                for b in J:
                    s = add[a][b]
                    if s not in J and s not in new_elements:
                        new_elements.add(s)
                for r in range(n):
                    m1 = mul[r][a]
                    if m1 not in J and m1 not in new_elements:
                        new_elements.add(m1)
                    m2 = mul[a][r]
                    if m2 not in J and m2 not in new_elements:
                        new_elements.add(m2)
            if new_elements:
                J.update(new_elements)
                changed = True
        if J.isdisjoint(S_set):
            return False
    return True

def is_completely_prime_ideal(n, add, mul, zero, P):
    if not is_ideal(n, add, mul, zero, P): return False
    P_set = set(P)
    if len(P_set) == n: return False
    for a in range(n):
        for b in range(n):
            if mul[a][b] in P_set:
                if a not in P_set and b not in P_set:
                    return False
    return True

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            S = witness['S']
            I = witness['I']
        elif hasattr(witness, 'n') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
            n = witness.n
            add = witness.add
            mul = witness.mul
            S = witness.S
            I = witness.I
        else:
            n, add, mul, S, I = witness
            
        if not is_ring(n, add, mul):
            return [False, False, False]
            
        zero = -1
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
                
        h1 = is_multiplicative_subset(n, mul, S)
        h2 = is_maximal_disjoint_ideal(n, add, mul, zero, S, I)
        neg_q = not is_completely_prime_ideal(n, add, mul, zero, I)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: S is a multiplicative subset of R",
    "H_2: I is an ideal of R that is maximal with respect to the property of being disjoint from S",
    "¬Q: The ideal I is not a prime ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2
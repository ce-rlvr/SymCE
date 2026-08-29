import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Setup named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def make_boolean_ring(n_vars):
    size = 1 << n_vars
    add = [[0]*size for _ in range(size)]
    mul = [[0]*size for _ in range(size)]
    for i in range(size):
        for j in range(size):
            add[i][j] = i ^ j
            mul[i][j] = i & j
    return {'add': add, 'mul': mul}

Z2_ring = make_boolean_ring(1)
Z2xZ2_ring = make_boolean_ring(2)
Z2xZ2xZ2_ring = make_boolean_ring(3)

def is_ring(add, mul):
    try:
        n = len(add)
        if n == 0: return False
        if len(mul) != n: return False
        if any(len(row) != n for row in add) or any(len(row) != n for row in mul): return False
        
        zero = None
        for e in range(n):
            if all(add[x][e] == x and add[e][x] == x for x in range(n)):
                zero = e
                break
        if zero is None: return False
        
        for i in range(n):
            if not any(add[i][j] == zero and add[j][i] == zero for j in range(n)):
                return False
                
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]: return False
                for k in range(n):
                    if add[i][add[j][k]] != add[add[i][j]][k]: return False
                    if mul[i][mul[j][k]] != mul[mul[i][j]][k]: return False
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
        return True
    except Exception:
        return False

def is_boolean_ring(add, mul):
    try:
        if not is_ring(add, mul): return False
        n = len(add)
        for i in range(n):
            if mul[i][i] != i: return False
        return True
    except Exception:
        return False

def has_identity(mul):
    try:
        n = len(mul)
        for e in range(n):
            if all(mul[x][e] == x and mul[e][x] == x for x in range(n)):
                return True
        return False
    except Exception:
        return False

def is_maximal_ideal(add, mul, P):
    try:
        P_set = set(P)
        if not P_set: return False
        n = len(add)
        if any(x not in range(n) for x in P_set): return False
        
        zero = None
        for e in range(n):
            if all(add[x][e] == x and add[e][x] == x for x in range(n)):
                zero = e
                break
        if zero is None or zero not in P_set: return False
        
        inv = [0]*n
        for i in range(n):
            for j in range(n):
                if add[i][j] == zero:
                    inv[i] = j
                    break
                    
        for a in P_set:
            for b in P_set:
                if add[a][inv[b]] not in P_set: return False
                
        for a in P_set:
            for r in range(n):
                if mul[a][r] not in P_set: return False
                if mul[r][a] not in P_set: return False
                
        if len(P_set) == n: return False
        
        for x in range(n):
            if x in P_set: continue
            
            gen = P_set.copy()
            gen.add(x)
            
            while True:
                new_gen = set(gen)
                for a in gen:
                    for b in gen:
                        new_gen.add(add[a][b])
                        new_gen.add(add[a][inv[b]])
                for a in gen:
                    for r in range(n):
                        new_gen.add(mul[a][r])
                        new_gen.add(mul[r][a])
                if len(new_gen) == len(gen):
                    break
                gen = new_gen
                
            if len(gen) < n:
                return False
                
        return True
    except Exception:
        return False

def conditions(witness):
    """
    witness can be:
      - a dict: {'add': [[...]], 'mul': [[...]], 'P': [...]}
      - a tuple: ({'add': [[...]], 'mul': [[...]]}, [...])
      - a tuple: ([[...]], [[...]], [...])
    """
    try:
        if isinstance(witness, dict):
            if 'add' in witness and 'mul' in witness and 'P' in witness:
                add = witness['add']
                mul = witness['mul']
                P = witness['P']
            else:
                return [False, False, False]
        elif isinstance(witness, tuple) or isinstance(witness, list):
            if len(witness) == 2 and isinstance(witness[0], dict):
                add = witness[0]['add']
                mul = witness[0]['mul']
                P = witness[1]
            elif len(witness) == 3:
                add, mul, P = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    h1 = is_boolean_ring(add, mul)
    
    try:
        h2 = has_identity(mul)
    except Exception:
        h2 = False
        
    try:
        q = is_maximal_ideal(add, mul, P)
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "H_2: R has a multiplicative identity",
    "¬Q: P is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2
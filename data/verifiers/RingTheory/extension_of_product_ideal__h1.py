import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: S is a commutative ring",
    "H_2: f is a ring homomorphism from R to S",
    "H_3: I is an ideal of R",
    "H_4: J is an ideal of R",
    "¬Q: (IJ)^e != I^e J^e"
]

N_HYP = 4
NEG_Q_INDEX = 4

def get_val(witness, name, default=None):
    if isinstance(witness, dict) and name in witness:
        return witness[name]
    elif hasattr(witness, name):
        return getattr(witness, name)
    return default

def is_ring(add, mul):
    n = len(add)
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False
    return True

def is_commutative_ring(add, mul):
    if not is_ring(add, mul): return False
    n = len(add)
    for i in range(n):
        for j in range(n):
            if mul[i][j] != mul[j][i]: return False
    return True

def is_homomorphism(R_add, R_mul, S_add, S_mul, f):
    n = len(R_add)
    for i in range(n):
        for j in range(n):
            if f[R_add[i][j]] != S_add[f[i]][f[j]]: return False
            if f[R_mul[i][j]] != S_mul[f[i]][f[j]]: return False
            
    id_R = -1
    for i in range(n):
        if all(R_mul[i][j] == j and R_mul[j][i] == j for j in range(n)):
            id_R = i
            break
    m = len(S_add)
    id_S = -1
    for i in range(m):
        if all(S_mul[i][j] == j and S_mul[j][i] == j for j in range(m)):
            id_S = i
            break
            
    if id_R != -1 and id_S != -1:
        if f[id_R] != id_S:
            return False
            
    return True

def is_ideal(add, mul, I):
    if not I: return False
    I_set = set(I)
    n = len(add)
    for i in I:
        for j in I:
            if add[i][j] not in I_set: return False
    for i in I:
        for r in range(n):
            if mul[i][r] not in I_set: return False
            if mul[r][i] not in I_set: return False
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero not in I_set: return False
    
    # Check additive inverse
    for i in I:
        has_inv = False
        for j in I:
            if add[i][j] == zero:
                has_inv = True
                break
        if not has_inv: return False
        
    return True

def generate_ideal(add, mul, generators):
    n = len(add)
    ideal = set(generators)
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if not ideal:
        return {zero} if zero != -1 else set()
    
    while True:
        new_ideal = set(ideal)
        for x in ideal:
            for y in ideal:
                new_ideal.add(add[x][y])
        for x in ideal:
            for r in range(n):
                new_ideal.add(mul[r][x])
                new_ideal.add(mul[x][r])
        if zero != -1:
            new_ideal.add(zero)
            for x in ideal:
                for y in range(n):
                    if add[x][y] == zero:
                        new_ideal.add(y)
        if len(new_ideal) == len(ideal):
            break
        ideal = new_ideal
    return ideal

def product_ideal(add, mul, I, J):
    n = len(add)
    generators = set()
    for i in I:
        for j in J:
            generators.add(mul[i][j])
    return generate_ideal(add, mul, generators)

def conditions(witness):
    try:
        R_add = get_val(witness, "R_add")
        R_mul = get_val(witness, "R_mul")
        S_add = get_val(witness, "S_add")
        S_mul = get_val(witness, "S_mul")
        f = get_val(witness, "f")
        I = get_val(witness, "I")
        J = get_val(witness, "J")
        
        if any(x is None for x in [R_add, R_mul, S_add, S_mul, f, I, J]):
            return [False] * 5
            
        h1 = is_commutative_ring(S_add, S_mul)
        h2 = is_ring(R_add, R_mul) and is_homomorphism(R_add, R_mul, S_add, S_mul, f)
        h3 = is_ideal(R_add, R_mul, I)
        h4 = is_ideal(R_add, R_mul, J)
        
        # Calculate IJ
        IJ = product_ideal(R_add, R_mul, I, J)
        
        # Calculate (IJ)^e
        IJ_e_gens = {f[x] for x in IJ}
        IJ_e = generate_ideal(S_add, S_mul, IJ_e_gens)
        
        # Calculate I^e and J^e
        I_e_gens = {f[x] for x in I}
        I_e = generate_ideal(S_add, S_mul, I_e_gens)
        
        J_e_gens = {f[x] for x in J}
        J_e = generate_ideal(S_add, S_mul, J_e_gens)
        
        # Calculate I^e J^e
        I_e_J_e = product_ideal(S_add, S_mul, I_e, J_e)
        
        neg_q = (IJ_e != I_e_J_e)
        
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        return [False] * 5
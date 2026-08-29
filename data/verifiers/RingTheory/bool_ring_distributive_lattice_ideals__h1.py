import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
def make_Zn(n):
    add_table = [[(i+j)%n for j in range(n)] for i in range(n)]
    mul_table = [[(i*j)%n for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)

def make_F2_x_y_mod_m2():
    """
    Constructs the ring F_2[x, y] / (x^2, xy, y^2).
    This is a local ring of size 8. Its maximal ideal m = (x, y) has m^2 = 0.
    The sub-ideals of m correspond to the vector subspaces of m, which form
    the non-distributive diamond lattice M_3.
    """
    n = 8
    add_table = [[0]*8 for _ in range(8)]
    mul_table = [[0]*8 for _ in range(8)]
    for i in range(8):
        for j in range(8):
            a1, b1, c1 = i&1, (i>>1)&1, (i>>2)&1
            a2, b2, c2 = j&1, (j>>1)&1, (j>>2)&1
            
            a3 = a1 ^ a2
            b3 = b1 ^ b2
            c3 = c1 ^ c2
            add_table[i][j] = a3 + b3*2 + c3*4
            
            a4 = a1 * a2
            b4 = a1 * b2 + b1 * a2
            c4 = a1 * c2 + c1 * a2
            
            a4 %= 2
            b4 %= 2
            c4 %= 2
            
            mul_table[i][j] = a4 + b4*2 + c4*4
    return (n, add_table, mul_table)

R_counterexample = make_F2_x_y_mod_m2()

def is_ring(witness):
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return False
        n, add_table, mul_table = witness
        if not isinstance(n, int) or n <= 0 or n > 64:
            return False
        if len(add_table) != n or len(mul_table) != n: return False
        for i in range(n):
            if len(add_table[i]) != n or len(mul_table[i]) != n: return False
            for j in range(n):
                if not (0 <= add_table[i][j] < n): return False
                if not (0 <= mul_table[i][j] < n): return False
        
        # Check abelian group under addition
        for i in range(n):
            if add_table[i][0] != i or add_table[0][i] != i: return False
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
        for i in range(n):
            has_inv = False
            for j in range(n):
                if add_table[i][j] == 0:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Check multiplication associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                    
        # Check distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False
                    
        return True
    except Exception:
        return False

def get_ideals(witness):
    n, add_table, mul_table = witness
    
    def add_subsets(A, B):
        res = set()
        for a in A:
            for b in B:
                res.add(add_table[a][b])
        return frozenset(res)
        
    def gen_ideal(S):
        I = set(S)
        I.add(0)
        changed = True
        while changed:
            changed = False
            new_I = set(I)
            for a in I:
                for b in I:
                    c = add_table[a][b]
                    if c not in new_I:
                        new_I.add(c)
            for a in I:
                for r in range(n):
                    c1 = mul_table[r][a]
                    c2 = mul_table[a][r]
                    if c1 not in new_I: new_I.add(c1)
                    if c2 not in new_I: new_I.add(c2)
            if len(new_I) > len(I):
                I = new_I
                changed = True
        return frozenset(I)
        
    principal_ideals = set()
    for i in range(n):
        principal_ideals.add(gen_ideal({i}))
        
    ideals = set(principal_ideals)
    changed = True
    while changed:
        changed = False
        new_ideals = set(ideals)
        for I1 in ideals:
            for I2 in ideals:
                I3 = add_subsets(I1, I2)
                if I3 not in new_ideals:
                    new_ideals.add(I3)
                    if len(new_ideals) > 100:
                        return set()
        if len(new_ideals) > len(ideals):
            ideals = new_ideals
            changed = True
            
    return ideals

def is_distributive(ideals, add_table):
    if not ideals:
        return True
    def add_ideals(A, B):
        res = set()
        for a in A:
            for b in B:
                res.add(add_table[a][b])
        return frozenset(res)
        
    ideals = list(ideals)
    for A in ideals:
        for B in ideals:
            for C in ideals:
                lhs = A.intersection(add_ideals(B, C))
                rhs = add_ideals(A.intersection(B), A.intersection(C))
                if lhs != rhs:
                    return False
    return True

def conditions(witness):
    try:
        h1 = is_ring(witness)
    except Exception:
        h1 = False
        
    try:
        if h1:
            ideals = get_ideals(witness)
            n, add_table, mul_table = witness
            neg_q = not is_distributive(ideals, add_table)
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let L be the set of all ideals of R",
    "¬Q: L does not form a distributive lattice under the operations of ideal addition and ideal intersection"
]

N_HYP = 1
NEG_Q_INDEX = 1
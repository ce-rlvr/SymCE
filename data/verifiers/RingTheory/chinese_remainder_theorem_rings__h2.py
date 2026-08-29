import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

# Top-level setup for standard algebra objects
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
    "H_1: R is a commutative ring with identity",
    "H_2: I + J = R",
    "¬Q: The quotient ring R/(I \\cap J) is not isomorphic to (R/I) \\times (R/J)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def parse_witness(witness):
    """
    Accepts witness in two formats:
    1. (n, I, J) where n is an int (representing Z/nZ), I and J are lists of ints.
    2. (R_elements, add_table, mul_table, I_elements, J_elements) for a custom finite ring.
    Returns (R_elements, add_table, mul_table, I_elements, J_elements) using integer indices.
    """
    if isinstance(witness, tuple) and len(witness) == 3:
        n, I, J = witness
        if not isinstance(n, int) or n <= 0:
            return None
        R_elements = list(range(n))
        add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
        mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
        return R_elements, add_table, mul_table, list(set(I)), list(set(J))
        
    elif isinstance(witness, tuple) and len(witness) == 5:
        R_elements, add_table, mul_table, I_elements, J_elements = witness
        n = len(R_elements)
        
        if len(add_table) != n or len(mul_table) != n:
            return None
            
        new_add = [[0]*n for _ in range(n)]
        new_mul = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                a_val = add_table[i][j]
                m_val = mul_table[i][j]
                if a_val in R_elements:
                    new_add[i][j] = R_elements.index(a_val)
                else:
                    return None
                if m_val in R_elements:
                    new_mul[i][j] = R_elements.index(m_val)
                else:
                    return None
                    
        new_I = []
        for x in I_elements:
            if x in R_elements:
                new_I.append(R_elements.index(x))
            else:
                return None
                
        new_J = []
        for x in J_elements:
            if x in R_elements:
                new_J.append(R_elements.index(x))
            else:
                return None
                
        return list(range(n)), new_add, new_mul, list(set(new_I)), list(set(new_J))
        
    return None

def is_commutative_ring_with_identity(n, add_table, mul_table):
    # Check commutativity of addition
    for i in range(n):
        for j in range(n):
            if add_table[i][j] != add_table[j][i]: return False
            
    # Check associativity of addition
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
                
    # Find additive identity (0)
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None: return False
    
    # Check additive inverse
    for i in range(n):
        if not any(add_table[i][j] == zero for j in range(n)): return False
        
    # Check commutativity of multiplication
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] != mul_table[j][i]: return False
            
    # Check associativity of multiplication
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                
    # Check distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                
    # Find multiplicative identity (1)
    one = None
    for i in range(n):
        if all(mul_table[i][j] == j for j in range(n)):
            one = i
            break
    if one is None: return False
    
    return True

def check_I_plus_J(n, add_table, I_elements, J_elements):
    sums = set()
    for i in I_elements:
        for j in J_elements:
            sums.add(add_table[i][j])
    return len(sums) == n

def is_ideal(n, add_table, mul_table, subset):
    if not subset: return False
    
    # Find zero
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None or zero not in subset: return False
    
    # Check subgroup under addition
    for x in subset:
        for y in subset:
            if add_table[x][y] not in subset: return False
            
    for x in subset:
        has_inv = False
        for y in subset:
            if add_table[x][y] == zero:
                if y in subset:
                    has_inv = True
                    break
        if not has_inv: return False
        
    # Check ideal property (two-sided)
    for x in subset:
        for r in range(n):
            if mul_table[r][x] not in subset: return False
            if mul_table[x][r] not in subset: return False
            
    return True

def check_conclusion(n, add_table, mul_table, I_elements, J_elements):
    # If I or J is not an ideal, the quotient rings are undefined, so they cannot be isomorphic.
    if not is_ideal(n, add_table, mul_table, I_elements):
        return False
    if not is_ideal(n, add_table, mul_table, J_elements):
        return False
        
    I_cap_J = list(set(I_elements) & set(J_elements))
    
    size_R = n
    size_I = len(I_elements)
    size_J = len(J_elements)
    size_I_cap_J = len(I_cap_J)
    
    if size_I == 0 or size_J == 0 or size_I_cap_J == 0:
        return False
        
    size_mod_I = size_R // size_I
    size_mod_J = size_R // size_J
    size_mod_I_cap_J = size_R // size_I_cap_J
    
    # For finite rings, if I and J are ideals, the canonical map is an isomorphism
    # if and only if the sizes of the domain and codomain match.
    if size_mod_I_cap_J != size_mod_I * size_mod_J:
        return False
        
    return True

def conditions(witness):
    try:
        parsed = parse_witness(witness)
        if parsed is None:
            return [False, False, False]
            
        R_elements, add_table, mul_table, I_elements, J_elements = parsed
        n = len(R_elements)
        
        h1 = is_commutative_ring_with_identity(n, add_table, mul_table)
        h2 = check_I_plus_J(n, add_table, I_elements, J_elements)
        
        # neg_Q is True if the conclusion fails
        neg_q = not check_conclusion(n, add_table, mul_table, I_elements, J_elements)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]
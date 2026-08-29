import itertools
import math
import functools
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def parse_witness(witness):
    """
    Extracts the finite ring and ideals from the witness.
    Expected format: (n, add_table, mul_table, I_elements, J_elements)
    """
    if isinstance(witness, dict):
        return witness['n'], witness['add'], witness['mul'], witness['I'], witness['J']
    elif isinstance(witness, (tuple, list)):
        return witness[0], witness[1], witness[2], witness[3], witness[4]
    else:
        return witness.n, witness.add, witness.mul, witness.I, witness.J

def is_commutative_ring(n, add, mul):
    if n <= 0: 
        return False
    
    # Check bounds
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n): return False
            if not (0 <= mul[i][j] < n): return False
            
    # Addition is commutative
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False
            
    # Addition is associative
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False
                
    # 0 is additive identity
    for i in range(n):
        if add[i][0] != i or add[0][i] != i: return False
        
    # Additive inverse exists
    for i in range(n):
        has_inv = False
        for j in range(n):
            if add[i][j] == 0:
                has_inv = True
                break
        if not has_inv: return False
        
    # Multiplication is commutative
    for i in range(n):
        for j in range(n):
            if mul[i][j] != mul[j][i]: return False
            
    # Multiplication is associative
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
                
    # Distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                
    return True

def is_ideal(n, add, mul, subset):
    if not subset: 
        return False
    subset = set(subset)
    
    # Closed under addition
    for a in subset:
        for b in subset:
            if add[a][b] not in subset: return False
            
    # Closed under multiplication by R
    for a in subset:
        for r in range(n):
            if mul[r][a] not in subset: return False
            if mul[a][r] not in subset: return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        n, add, mul, I, J = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring and I, J are ideals
    try:
        h1 = is_commutative_ring(n, add, mul) and is_ideal(n, add, mul, I) and is_ideal(n, add, mul, J)
    except Exception:
        h1 = False
        
    # H_2: I + J = R
    try:
        I_set = set(I)
        J_set = set(J)
        sum_set = set()
        for a in I_set:
            for b in J_set:
                sum_set.add(add[a][b])
        h2 = (sum_set == set(range(n)))
    except Exception:
        h2 = False
        
    # ¬Q: IJ != I \cap J
    try:
        I_set = set(I)
        J_set = set(J)
        
        # Compute the set of all products ab for a in I, b in J
        products = set()
        for a in I_set:
            for b in J_set:
                products.add(mul[a][b])
                
        # The ideal IJ is the additive closure of these products
        closure = set(products)
        changed = True
        while changed:
            changed = False
            new_elements = set()
            for a in closure:
                for b in closure:
                    s = add[a][b]
                    if s not in closure:
                        new_elements.add(s)
            if new_elements:
                closure.update(new_elements)
                changed = True
                
        IJ = closure
        I_cap_J = I_set.intersection(J_set)
        
        neg_q = (IJ != I_cap_J)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring and I, J are ideals",
    "H_2: I + J = R",
    "¬Q: IJ != I \\cap J"
]

N_HYP = 2
NEG_Q_INDEX = 2
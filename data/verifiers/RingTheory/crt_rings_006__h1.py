import sympy
from sympy import Matrix, ImmutableMatrix, eye, zeros
from itertools import product

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def to_immutable(S):
    """Convert elements to an immutable and hashable form if possible."""
    res = set()
    for s in S:
        if hasattr(s, 'as_immutable'):
            res.add(s.as_immutable())
        else:
            res.add(s)
    return res

def is_ring(R):
    """Check if R is a valid ring (closed under operations, associative, distributive, has 0)."""
    if not R: 
        return False
    
    # Closure under addition, subtraction, and multiplication
    for a in R:
        for b in R:
            if (a + b) not in R: return False
            if (a - b) not in R: return False
            if (a * b) not in R: return False
            
    # Commutativity of addition
    for a in R:
        for b in R:
            if (a + b) != (b + a): return False
            
    # Associativity and Distributivity
    for a in R:
        for b in R:
            for c in R:
                if ((a + b) + c) != (a + (b + c)): return False
                if ((a * b) * c) != (a * (b * c)): return False
                if (a * (b + c)) != ((a * b) + (a * c)): return False
                if ((a + b) * c) != ((a * c) + (b * c)): return False
                
    # Existence of additive identity
    has_zero = False
    for z in R:
        is_z = True
        for a in R:
            if (a + z) != a:
                is_z = False
                break
        if is_z:
            has_zero = True
            break
            
    return has_zero

def is_ideal(I, R):
    """Check if I is a two-sided ideal of R."""
    if not I.issubset(R): 
        return False
    if not I: 
        return False
        
    # Additive subgroup (closed under subtraction)
    for a in I:
        for b in I:
            if (a - b) not in I: 
                return False
                
    # Absorbing property on both sides
    for i in I:
        for r in R:
            if (i * r) not in I: return False
            if (r * i) not in I: return False
            
    return True

def additive_closure(S):
    """Compute the closure of a set S under addition and subtraction."""
    closure = set(S)
    added = True
    while added:
        added = False
        new_elements = set()
        for a in closure:
            for b in closure:
                new_elements.add(a + b)
                new_elements.add(a - b)
        for e in new_elements:
            if e not in closure:
                closure.add(e)
                added = True
    return closure

def ideal_power(I, m):
    """Compute the m-th power of an ideal I."""
    if m <= 0:
        raise ValueError("Power must be positive")
    if m == 1:
        return I
        
    prods = set()
    for p in product(I, repeat=m):
        res = p[0]
        for x in p[1:]:
            res = res * x
        prods.add(res)
        
    return additive_closure(prods)

def conditions(witness):
    """
    Check the hypotheses and the negated conclusion for the conjecture.
    Witness should be a tuple: (R, I, J, m, n)
    where R, I, J are iterables of ring elements (e.g., SymPy matrices).
    """
    try:
        R, I, J, m, n = witness
    except Exception:
        return [False, False, False, False]
    
    try:
        R_imm = to_immutable(R)
        I_imm = to_immutable(I)
        J_imm = to_immutable(J)
    except Exception:
        return [False, False, False, False]
        
    # H_1: I and J are ideals of R
    try:
        h1 = is_ring(R_imm) and is_ideal(I_imm, R_imm) and is_ideal(J_imm, R_imm)
    except Exception:
        h1 = False
        
    # H_2: I + J = R
    try:
        I_plus_J = set()
        for i in I_imm:
            for j in J_imm:
                I_plus_J.add(i + j)
        h2 = (I_plus_J == R_imm)
    except Exception:
        h2 = False
        
    # H_3: m and n are positive integers
    try:
        h3 = isinstance(m, int) and isinstance(n, int) and m > 0 and n > 0
    except Exception:
        h3 = False
        
    # ¬Q: I^m + J^n != R
    try:
        Im = ideal_power(I_imm, m)
        Jn = ideal_power(J_imm, n)
        
        Im_plus_Jn = set()
        for i in Im:
            for j in Jn:
                Im_plus_Jn.add(i + j)
                
        neg_q = (Im_plus_Jn != R_imm)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "H_2: I + J = R",
    "H_3: m and n are positive integers",
    "¬Q: I^m + J^n != R"
]

N_HYP = 3
NEG_Q_INDEX = 3
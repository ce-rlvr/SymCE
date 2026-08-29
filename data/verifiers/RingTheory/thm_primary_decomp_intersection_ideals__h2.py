import sympy
import math
import functools

# Top-level setup for potential witness expressions
x, y, z = sympy.symbols('x y z')

def is_int(val):
    return isinstance(val, int) or isinstance(val, sympy.Integer)

def is_primary(n):
    """Check if the ideal (n) is primary in Z."""
    try:
        n = abs(int(n))
    except Exception:
        return False
    if n == 0:
        return True
    if n == 1:
        return False
    f = sympy.factorint(n)
    return len(f) == 1

def get_lcm(lst):
    """Compute the LCM of a list of integers, representing ideal intersection in Z."""
    if not lst:
        return 1
    val = 1
    for item in lst:
        val = sympy.lcm(val, int(item))
    return val

def is_irredundant_primary_decomposition(N, L):
    """Check if L is an irredundant primary decomposition of (N) in Z."""
    if not isinstance(L, (list, tuple)):
        return False
    if not all(is_primary(q) for q in L):
        return False
    
    # Check intersection equals N
    if N != 0:
        if abs(int(N)) != abs(get_lcm(L)):
            return False
    else:
        if list(L) != [0]:
            return False
            
    # Check irredundancy: 1. Distinct radicals
    rads = []
    for q in L:
        if q == 0:
            rads.append(0)
        else:
            rads.append(math.prod(sympy.factorint(abs(int(q))).keys()))
    if len(set(rads)) != len(L):
        return False
        
    # Check irredundancy: 2. None can be omitted
    for i in range(len(L)):
        sub = list(L[:i]) + list(L[i+1:])
        if not sub:
            continue
        if abs(int(N)) == abs(get_lcm(sub)):
            return False
            
    return True

def conditions(witness):
    """
    Given a witness, checks if it satisfies the hypotheses and falsifies the conclusion.
    Expected witness formats (representing ideals in Z):
      - (I, J, Q_list, P_list)
      - (Q_list, P_list)
      - {'I': I, 'J': J, 'Q_list': Q_list, 'P_list': P_list}
    """
    try:
        if isinstance(witness, dict):
            Q_list = witness.get('Q_list', witness.get('Q', []))
            P_list = witness.get('P_list', witness.get('P', []))
            I = witness.get('I', get_lcm(Q_list))
            J = witness.get('J', get_lcm(P_list))
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            I, J, Q_list, P_list = witness
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            Q_list, P_list = witness
            I = get_lcm(Q_list)
            J = get_lcm(P_list)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]
        
    # H_1: R is a commutative ring
    # We evaluate this in Z, which is a commutative ring.
    try:
        h1 = is_int(I) and is_int(J) and \
             all(is_int(q) for q in Q_list) and \
             all(is_int(p) for p in P_list)
    except Exception:
        h1 = False
        
    # H_2: I has a primary decomposition I = Q_1 \cap \dots \cap Q_n
    try:
        h2 = is_irredundant_primary_decomposition(I, Q_list)
    except Exception:
        h2 = False
        
    # H_3: J has a primary decomposition J = P_1 \cap \dots \cap P_m
    try:
        h3 = is_irredundant_primary_decomposition(J, P_list)
    except Exception:
        h3 = False
        
    # ¬Q: The intersection of all Q_i and P_k is NOT a primary decomposition of I \cap J
    try:
        combined = list(Q_list) + list(P_list)
        I_cap_J = get_lcm([I, J])
        neg_q = not is_irredundant_primary_decomposition(I_cap_J, combined)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I has a primary decomposition I = Q_1 \\cap \\dots \\cap Q_n",
    "H_3: J has a primary decomposition J = P_1 \\cap \\dots \\cap P_m",
    "¬Q: The intersection of all Q_i and P_k is NOT a primary decomposition of I \\cap J"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
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

def extract_p_d(witness):
    """Safely extract p and d from various possible witness formats."""
    try:
        if isinstance(witness, dict):
            return witness.get('p', None), witness.get('d', None)
        elif hasattr(witness, 'p') and hasattr(witness, 'd'):
            return witness.p, witness.d
        elif isinstance(witness, (list, tuple)) and len(witness) == 2:
            return witness[0], witness[1]
    except Exception:
        pass
    return None, None

def exactly_one_subfield(p, d):
    """
    Returns True if there is exactly one subfield of Q(zeta_p) of degree d over Q.
    This is equivalent to checking if the Galois group (Z/pZ)* has exactly one subgroup of index d.
    """
    if p <= 0 or d <= 0:
        return False
        
    # Find the invariant factors of the Galois group (Z/pZ)*
    factors = factorint(p)
    orders = []
    for q_prime, a in factors.items():
        if q_prime == 2:
            if a == 2:
                orders.append(2)
            elif a >= 3:
                orders.append(2)
                orders.append(2**(a-2))
        else:
            orders.append((q_prime - 1) * (q_prime**(a-1)))
            
    # Degree of the extension Q(zeta_p) / Q is phi(p)
    order_G = 1
    for ord in orders:
        order_G *= ord
    
    # If d does not divide the degree, there are 0 subfields of degree d
    if order_G % d != 0:
        return False
        
    G_factors = factorint(order_G)
    d_factors = factorint(d)
    
    # A finite abelian group has exactly 1 subgroup of index d iff for every prime l dividing its order,
    # the Sylow l-subgroup is either cyclic, or the l-part of d is trivial (v=0) or maximal (v=V).
    for l, V in G_factors.items():
        v = d_factors.get(l, 0)
        if 0 < v < V:
            # Check if the Sylow l-subgroup is cyclic
            # It is cyclic iff at most one cyclic factor of (Z/pZ)* has an order divisible by l
            count = sum(1 for ord in orders if ord % l == 0)
            if count > 1:
                return False
                
    return True

def conditions(witness) -> list[bool]:
    p, d = extract_p_d(witness)
    
    # H_1: p is an odd prime number
    try:
        p_val = int(p)
        h1 = sympy.isprime(p_val) and p_val % 2 != 0
    except Exception:
        h1 = False
        
    # H_2: d is a positive integer that divides p-1
    try:
        p_val = int(p)
        d_val = int(d)
        h2 = (d_val > 0) and ((p_val - 1) % d_val == 0)
    except Exception:
        h2 = False
        
    # ¬Q: There does NOT exist exactly one subfield K of Q(zeta_p) such that [K : Q] = d
    try:
        p_val = int(p)
        d_val = int(d)
        neg_q = not exactly_one_subfield(p_val, d_val)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: d is a positive integer that divides p-1",
    "not Q: There does not exist exactly one subfield K of Q(zeta_p) of degree d"
]

N_HYP = 2
NEG_Q_INDEX = 2
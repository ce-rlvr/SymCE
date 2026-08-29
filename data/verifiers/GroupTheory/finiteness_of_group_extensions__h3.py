import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo, Integer

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
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: The quotient group G/N is a finite group",
    "¬Q: G is not a finite group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def check_is_group(G):
    if hasattr(G, 'is_group'):
        val = G.is_group
        return val() if callable(val) else val
    if hasattr(G, 'is_Group'):
        val = G.is_Group
        return val() if callable(val) else val
    type_name = type(G).__name__
    if 'Group' in type_name:
        return True
    return False

def check_is_normal(G, N):
    if hasattr(G, 'is_normal'):
        return G.is_normal(N)
    if hasattr(G, 'is_normal_subgroup'):
        return G.is_normal_subgroup(N)
    if hasattr(N, 'is_normal_in'):
        return N.is_normal_in(G)
    return False

def check_is_finite(G):
    if hasattr(G, 'is_finite'):
        val = G.is_finite
        return val() if callable(val) else val
    if hasattr(G, 'order'):
        val = G.order
        ord_val = val() if callable(val) else val
        return ord_val < oo and ord_val != oo
    return False

def check_quotient_is_finite(G, N):
    if hasattr(G, 'quotient_is_finite'):
        return G.quotient_is_finite(N)
    if hasattr(G, 'quotient_group'):
        Q = G.quotient_group(N)
        return check_is_finite(Q)
    if hasattr(G, 'quotient'):
        Q = G.quotient(N)
        return check_is_finite(Q)
    return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The standard counterexample is G = Z, N = nZ (e.g., n=2).
    This verifier supports an integer representation where an integer k represents the group kZ under addition.
    """
    G, N = None, None
    
    # Try to unpack witness as a tuple (G, N) or an object with G and N attributes
    if isinstance(witness, tuple) and len(witness) == 2:
        G, N = witness
    elif hasattr(witness, 'G') and hasattr(witness, 'N'):
        G = witness.G
        N = witness.N

    if G is not None and N is not None:
        # Special case: integers representing k*Z under addition
        if isinstance(G, (int, Integer)) and isinstance(N, (int, Integer)):
            G_val, N_val = int(G), int(N)
            
            # H1: kZ is always a group under addition
            h1 = True
            
            # H2: N is a normal subgroup of G iff N is a subset of G (i.e., N is a multiple of G)
            if G_val == 0:
                h2 = (N_val == 0)
            else:
                h2 = (N_val % G_val == 0)
                
            # H3: G/N is finite iff N != 0 or G == 0
            h3 = (N_val != 0 or G_val == 0)
            
            # ¬Q: G is not finite iff G != 0
            neg_q = (G_val != 0)
            
            return [h1, h2, h3, neg_q]

        # General object case (e.g., SymPy groups or custom objects)
        try:
            h1 = bool(check_is_group(G))
        except Exception:
            h1 = False
            
        try:
            h2 = bool(check_is_normal(G, N))
        except Exception:
            h2 = False
            
        try:
            h3 = bool(check_quotient_is_finite(G, N))
        except Exception:
            h3 = False
            
        try:
            neg_q = not bool(check_is_finite(G))
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]

    # Fallback: witness itself directly implements the properties
    try:
        h1 = bool(witness.is_group)
    except Exception:
        h1 = False
        
    try:
        h2 = bool(witness.is_normal_subgroup)
    except Exception:
        h2 = False
        
    try:
        h3 = bool(witness.quotient_is_finite)
    except Exception:
        h3 = False
        
    try:
        neg_q = not bool(witness.is_finite)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]
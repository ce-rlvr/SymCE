import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Given a witness tuple (G, N), checks if it is a valid counterexample to the conjecture.
    """
    try:
        G, N = witness
    except Exception:
        return [False, False]
        
    # H_1: N is a normal subgroup of G
    h1_ok = False
    try:
        if hasattr(G, 'is_normal'):
            h1_ok = bool(G.is_normal(N))
        elif hasattr(N, 'is_normal'):
            h1_ok = bool(N.is_normal(G))
        elif hasattr(G, 'is_normal_subgroup'):
            h1_ok = bool(G.is_normal_subgroup(N))
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: The order of the quotient group G/N is not equal to |G| / |N|
    neg_q_ok = False
    try:
        # Get order of G
        if hasattr(G, 'order'):
            order_G = G.order
            if callable(order_G):
                order_G = order_G()
        else:
            order_G = len(G)
            
        # Get order of N
        if hasattr(N, 'order'):
            order_N = N.order
            if callable(order_N):
                order_N = order_N()
        else:
            order_N = len(N)
            
        # Get quotient group G/N
        if hasattr(G, 'quotient_group'):
            Q_grp = G.quotient_group(N)
        elif hasattr(G, 'quotient'):
            Q_grp = G.quotient(N)
        else:
            Q_grp = G / N
            
        # Get order of G/N
        if hasattr(Q_grp, 'order'):
            order_Q = Q_grp.order
            if callable(order_Q):
                order_Q = order_Q()
        else:
            order_Q = len(Q_grp)
            
        expected = order_G / order_N
        
        # If expected is nan (e.g. oo / oo), it is not equal to any well-defined quotient order
        if expected is sympy.nan:
            neg_q_ok = True
        else:
            neg_q_ok = bool(order_Q != expected)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: The order of the quotient group G/N is not equal to |G| / |N|"
]

N_HYP = 1
NEG_Q_INDEX = 1
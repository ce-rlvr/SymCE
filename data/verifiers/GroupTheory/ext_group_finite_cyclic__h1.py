import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Standard group theory objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_cyclic_group(G):
    try:
        if hasattr(G, 'is_cyclic'):
            val = G.is_cyclic() if callable(G.is_cyclic) else G.is_cyclic
            if val is not None:
                return bool(val)
    except Exception:
        pass
    
    try:
        order = G.order() if callable(getattr(G, 'order', None)) else G.order
        for g in G.elements:
            g_order = g.order() if callable(getattr(g, 'order', None)) else g.order
            if g_order == order:
                return True
        return False
    except Exception:
        return False

def is_abelian_group(A):
    try:
        if hasattr(A, 'is_abelian'):
            val = A.is_abelian() if callable(A.is_abelian) else A.is_abelian
            if val is not None:
                return bool(val)
    except Exception:
        pass
    
    try:
        if not hasattr(A, 'elements') or not hasattr(A, 'order'):
            return False
            
        elements = list(A.elements)
        for a in elements:
            for b in elements:
                if a * b != b * a:
                    return False
        return True
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The true theorem states that for any abelian group A, Ext^1(G, A) is isomorphic to A/nA.
    The conjecture drops the hypothesis that A is an abelian group.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                n, G, A = witness
            elif len(witness) == 2:
                n, G = witness
                A = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = (isinstance(n, int) or isinstance(n, sympy.Integer)) and n > 0
    except Exception:
        h1 = False
        
    # H2: G is a cyclic group of order n
    try:
        order = G.order() if callable(getattr(G, 'order', None)) else G.order
        h2 = (order == n) and is_cyclic_group(G)
    except Exception:
        h2 = False
        
    # ¬Q: The first Ext group Ext^1(G, A) is not isomorphic to A/nA
    # This occurs when A is not an abelian group (so Ext^1 is undefined or A/nA is undefined).
    try:
        if A is None:
            neg_q = True
        else:
            neg_q = not is_abelian_group(A)
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is a cyclic group of order n",
    "¬Q: The first Ext group Ext^1(G, A) is not isomorphic to A/nA"
]

N_HYP = 2
NEG_Q_INDEX = 2
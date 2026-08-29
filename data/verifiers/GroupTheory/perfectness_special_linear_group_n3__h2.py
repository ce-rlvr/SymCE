import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (n, F, G)
    where n is an integer, F is a field (or its prime power size), and G is the group SL(n, F).
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        n, F, G = witness
    except Exception:
        return [False, False, False, False]

    # H_1: n is an integer
    try:
        n_val = int(n)
        h1 = (n_val == n) and (n_val >= 1)
        n = n_val
    except Exception:
        h1 = False

    # H_2: F is a field
    try:
        if hasattr(F, 'order'):
            q = F.order
            if callable(q): q = q()
        elif hasattr(F, 'mod'):
            q = F.mod
            if callable(q): q = q()
        else:
            q = int(F)
            if q != F:
                q = None
        
        if q is not None and int(q) > 1:
            q = int(q)
            factors = factorint(q)
            h2 = len(factors) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: G is the special linear group SL(n, F)
    try:
        if not h1 or not h2:
            h3 = False
        else:
            expected_order = q**(n*(n-1)//2)
            for i in range(2, n+1):
                expected_order *= (q**i - 1)
            
            if hasattr(G, 'order'):
                g_order = G.order() if callable(G.order) else G.order
            else:
                g_order = None

            if g_order == expected_order:
                if n == 2 and q == 2:
                    is_ab = G.is_abelian
                    if callable(is_ab):
                        is_ab = is_ab()
                    h3 = not is_ab
                elif n == 2 and q == 3:
                    if hasattr(G, 'elements'):
                        elements = G.elements
                    else:
                        elements = list(G.generate())
                    order_2_count = 0
                    for g in elements:
                        g_ord = g.order() if callable(g.order) else g.order
                        if g_ord == 2:
                            order_2_count += 1
                    h3 = (order_2_count == 1)
                else:
                    h3 = True
            else:
                h3 = False
    except Exception:
        h3 = False

    # neg_Q: The commutator subgroup of G is not equal to G
    try:
        if hasattr(G, 'derived_subgroup'):
            C = G.derived_subgroup()
            if callable(C):
                C = C()
            
            if hasattr(C, 'order'):
                c_order = C.order() if callable(C.order) else C.order
            else:
                c_order = None
            
            if hasattr(G, 'order'):
                g_order = G.order() if callable(G.order) else G.order
            else:
                g_order = None
                
            neg_q = (c_order != g_order)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: F is a field",
    "H_3: G is the special linear group SL(n, F)",
    "¬Q: The commutator subgroup of G is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3
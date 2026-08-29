import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.ntheory import factorint

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def sl_order(n, m):
    """Computes the order of the special linear group SL(n, Z/mZ)."""
    try:
        m = int(m)
    except Exception:
        return None
    if m < 1:
        return None
    factors = factorint(m)
    order = 1
    for p, k in factors.items():
        p_order = p**(n*(n-1)//2)
        for i in range(2, n+1):
            p_order *= (p**i - 1)
        order *= p_order * p**((k-1)*(n**2 - 1))
    return order

def conditions(witness) -> list[bool]:
    # Extract n, F, G from the witness
    if isinstance(witness, dict):
        n = witness.get('n')
        F = witness.get('F')
        G = witness.get('G')
    elif isinstance(witness, tuple) and len(witness) == 3:
        n, F, G = witness
    else:
        n = getattr(witness, 'n', None)
        F = getattr(witness, 'F', None)
        G = getattr(witness, 'G', None)

    # H_1: n is an integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) or (hasattr(n, 'is_integer') and n.is_integer)
        if h1:
            n = int(n)
    except Exception:
        h1 = False

    # H_2: n >= 3
    try:
        h2 = h1 and (n >= 3)
    except Exception:
        h2 = False

    # H_3: G is the special linear group SL(n, F)
    try:
        h3 = False
        if hasattr(witness, 'is_SL'):
            h3 = bool(witness.is_SL() if callable(witness.is_SL) else witness.is_SL)
        elif hasattr(G, 'is_SL'):
            h3 = bool(G.is_SL(n, F) if callable(G.is_SL) else G.is_SL)
        elif hasattr(G, 'name') and isinstance(G.name, str) and 'SL' in G.name:
            h3 = True
        elif hasattr(G, 'order'):
            expected_order = sl_order(n, F)
            if expected_order is not None and G.order() == expected_order:
                h3 = True
    except Exception:
        h3 = False

    # ¬Q: The commutator subgroup of G is not equal to G (i.e., G is not perfect)
    try:
        neg_q = False
        if hasattr(witness, 'is_perfect'):
            neg_q = not (witness.is_perfect() if callable(witness.is_perfect) else witness.is_perfect)
        elif hasattr(G, 'is_perfect'):
            neg_q = not (G.is_perfect() if callable(G.is_perfect) else G.is_perfect)
        elif hasattr(G, 'derived_subgroup'):
            D = G.derived_subgroup()
            neg_q = (D.order() != G.order())
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "H_2: n >= 3",
    "H_3: G is the special linear group SL(n, F)",
    "¬Q: The commutator subgroup of G is not equal to G"
]

N_HYP = 3
NEG_Q_INDEX = 3
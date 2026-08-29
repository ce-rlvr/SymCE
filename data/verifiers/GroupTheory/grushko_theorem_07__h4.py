import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_fg_group(G):
    if hasattr(G, 'is_finitely_generated'):
        val = G.is_finitely_generated() if callable(G.is_finitely_generated) else G.is_finitely_generated
        if val is not None: 
            return bool(val)
    if hasattr(G, 'is_fg'):
        val = G.is_fg() if callable(G.is_fg) else G.is_fg
        if val is not None: 
            return bool(val)
    if hasattr(G, 'generators'):
        return True
    if type(G).__name__ in ['PermutationGroup', 'FpGroup', 'FreeGroup']:
        return True
    if hasattr(G, 'is_group'):
        val = G.is_group() if callable(G.is_group) else G.is_group
        if val: 
            return True
    return False

def is_free_product(G, H, P):
    if hasattr(P, 'is_free_product'):
        val = P.is_free_product(G, H) if callable(P.is_free_product) else P.is_free_product
        if val is not None: 
            return bool(val)
    if hasattr(P, 'is_free_product_of'):
        return bool(P.is_free_product_of(G, H))
    if hasattr(P, 'factors'):
        return P.factors == (G, H) or P.factors == [G, H]
    if hasattr(P, 'components'):
        return P.components == (G, H) or P.components == [G, H]
    if hasattr(P, 'G') and hasattr(P, 'H'):
        if P.G == G and P.H == H:
            return True
    
    # SymPy FpGroup heuristic
    if type(G).__name__ == 'FpGroup' and type(H).__name__ == 'FpGroup' and type(P).__name__ == 'FpGroup':
        if len(P.generators) == len(G.generators) + len(H.generators):
            return True
            
    return False

def get_rank(G):
    if hasattr(G, 'rank'):
        return G.rank() if callable(G.rank) else G.rank
    if hasattr(G, 'minimal_generators'):
        return len(G.minimal_generators())
    if hasattr(G, 'generators'):
        return len(G.generators)
    raise ValueError("Cannot determine rank")

def conditions(witness) -> list[bool]:
    # Extract G, H, and the free product P from the witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            P = witness.get('P', witness.get('G_star_H'))
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                G, H, P = witness
            else:
                return [False, False, False, False]
        else:
            G = witness.G
            H = witness.H
            P = getattr(witness, 'P', getattr(witness, 'G_star_H', None))
    except Exception:
        return [False, False, False, False]

    if P is None:
        return [False, False, False, False]

    # H_1: G is a finitely generated group
    try:
        h1_ok = is_fg_group(G)
    except Exception:
        h1_ok = False

    # H_2: H is a finitely generated group
    try:
        h2_ok = is_fg_group(H)
    except Exception:
        h2_ok = False

    # H_3: G * H is the free product of G and H
    try:
        h3_ok = is_free_product(G, H, P)
    except Exception:
        h3_ok = False

    # ¬Q: rank(G * H) != rank(G) + rank(H)
    try:
        rank_G = get_rank(G)
        rank_H = get_rank(H)
        rank_P = get_rank(P)
        neg_q_ok = bool(rank_P != rank_G + rank_H)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finitely generated group",
    "H_2: H is a finitely generated group",
    "H_3: G * H is the free product of G and H",
    "¬Q: rank(G * H) != rank(G) + rank(H)"
]

N_HYP = 3
NEG_Q_INDEX = 3
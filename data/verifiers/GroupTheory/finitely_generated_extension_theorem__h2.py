import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    "H_2: N is a finitely generated group",
    "H_3: The quotient group G/N is a finitely generated group",
    "¬Q: G is not a finitely generated group"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    # Handle dictionary witness
    if isinstance(witness, dict):
        try:
            if 'G_is_group' in witness or 'G_is_finitely_generated' in witness:
                h1 = bool(witness.get('G_is_group', False))
                h2 = bool(witness.get('N_is_finitely_generated', False))
                h3 = bool(witness.get('quotient_is_finitely_generated', False))
                neg_q = not bool(witness.get('G_is_finitely_generated', True))
                return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Extract G and N
    if isinstance(witness, tuple) and len(witness) == 2:
        G, N = witness
    else:
        G = getattr(witness, 'G', witness)
        N = getattr(witness, 'N', None)

    # H_1: G is a group
    try:
        if hasattr(G, 'is_group'):
            h1 = G.is_group() if callable(G.is_group) else G.is_group
        else:
            h1 = hasattr(G, 'generators') or hasattr(G, 'identity') or hasattr(G, 'group')
    except Exception:
        h1 = False

    # H_2: N is a finitely generated group
    try:
        if hasattr(N, 'is_finitely_generated'):
            h2 = N.is_finitely_generated() if callable(N.is_finitely_generated) else N.is_finitely_generated
        else:
            if hasattr(N, 'generators'):
                gens = N.generators
                h2 = len(gens) < float('inf') if hasattr(gens, '__len__') else True
            else:
                h2 = False
    except Exception:
        h2 = False

    # H_3: The quotient group G/N is a finitely generated group
    try:
        if hasattr(witness, 'quotient_is_finitely_generated'):
            h3 = witness.quotient_is_finitely_generated() if callable(witness.quotient_is_finitely_generated) else witness.quotient_is_finitely_generated
        else:
            if hasattr(witness, 'G_mod_N'):
                Q = witness.G_mod_N
            elif hasattr(G, 'quotient'):
                Q = G.quotient(N)
            else:
                Q = G / N
            
            if hasattr(Q, 'is_finitely_generated'):
                h3 = Q.is_finitely_generated() if callable(Q.is_finitely_generated) else Q.is_finitely_generated
            else:
                if hasattr(Q, 'generators'):
                    gens = Q.generators
                    h3 = len(gens) < float('inf') if hasattr(gens, '__len__') else True
                else:
                    h3 = False
    except Exception:
        h3 = False

    # ¬Q: G is not a finitely generated group
    try:
        if hasattr(G, 'is_finitely_generated'):
            g_fg = G.is_finitely_generated() if callable(G.is_finitely_generated) else G.is_finitely_generated
        else:
            if hasattr(G, 'generators'):
                gens = G.generators
                g_fg = len(gens) < float('inf') if hasattr(gens, '__len__') else True
            else:
                g_fg = False
        neg_q = not g_fg
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
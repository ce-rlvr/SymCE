import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
    "H_1: G is an abelian group",
    "H_2: G is finitely generated",
    "¬Q: The quotient group G/H is not finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    # Handle dictionary-based mock witnesses
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('G_is_abelian', False))
            h2 = bool(witness.get('G_is_finitely_generated', False))
            neg_q = not bool(witness.get('quotient_is_finitely_generated', True))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # Extract G and H from the witness
    try:
        if hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            G = witness
            H = None
    except Exception:
        return [False, False, False]

    # H_1: G is an abelian group
    try:
        if hasattr(G, 'is_abelian'):
            val = G.is_abelian
            h1 = bool(val() if callable(val) else val)
        elif hasattr(G, 'is_commutative'):
            val = G.is_commutative
            h1 = bool(val() if callable(val) else val)
    except Exception:
        pass

    # H_2: G is finitely generated
    try:
        if hasattr(G, 'is_finitely_generated'):
            val = G.is_finitely_generated
            h2 = bool(val() if callable(val) else val)
        elif hasattr(G, 'generators'):
            gens = G.generators
            if hasattr(gens, '__len__'):
                h2 = True
    except Exception:
        pass

    # ¬Q: The quotient group G/H is not finitely generated
    try:
        if hasattr(witness, 'quotient_is_finitely_generated'):
            val = witness.quotient_is_finitely_generated
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(G, 'quotient_is_finitely_generated'):
            val = G.quotient_is_finitely_generated
            neg_q = not bool(val(H) if callable(val) else val)
        elif H is not None:
            Q_grp = None
            if hasattr(G, 'quotient'):
                Q_grp = G.quotient(H)
            elif hasattr(G, 'quotient_group'):
                Q_grp = G.quotient_group(H)
            elif hasattr(G, '__truediv__'):
                try:
                    Q_grp = G / H
                except Exception:
                    pass
            
            if Q_grp is not None:
                if hasattr(Q_grp, 'is_finitely_generated'):
                    val = Q_grp.is_finitely_generated
                    neg_q = not bool(val() if callable(val) else val)
                elif hasattr(Q_grp, 'generators'):
                    gens = Q_grp.generators
                    if hasattr(gens, '__len__'):
                        neg_q = False
    except Exception:
        pass

    return [h1, h2, neg_q]
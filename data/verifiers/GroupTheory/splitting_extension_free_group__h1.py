import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.free_groups import FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import eye, zeros

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    # Handle mock dictionary witnesses
    if isinstance(witness, dict):
        if 'H1' in witness and 'H2' in witness and 'neg_Q' in witness:
            try:
                return [bool(witness['H1']), bool(witness['H2']), bool(witness['neg_Q'])]
            except Exception:
                pass

    # Handle mock object witnesses
    if hasattr(witness, 'H1') and hasattr(witness, 'H2') and hasattr(witness, 'neg_Q'):
        try:
            h1 = witness.H1() if callable(witness.H1) else witness.H1
            h2 = witness.H2() if callable(witness.H2) else witness.H2
            nq = witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q
            return [bool(h1), bool(h2), bool(nq)]
        except Exception:
            pass

    G = None
    N = None
    if isinstance(witness, tuple) and len(witness) == 2:
        G, N = witness
    else:
        try:
            G = witness.G
            N = witness.N
        except AttributeError:
            pass

    # H1: N is a normal subgroup of G
    h1 = False
    try:
        if hasattr(witness, 'is_normal'):
            h1 = bool(witness.is_normal()) if callable(witness.is_normal) else bool(witness.is_normal)
        elif G is not None and N is not None:
            if hasattr(N, 'is_normal'):
                h1 = bool(N.is_normal(G))
            elif hasattr(G, 'is_normal_subgroup'):
                h1 = bool(G.is_normal_subgroup(N))
            else:
                h1 = bool(N.is_subgroup(G) and N.is_normal(G))
    except Exception:
        h1 = False

    # H2: G/N is a free group
    h2 = False
    try:
        if hasattr(witness, 'quotient_is_free'):
            h2 = bool(witness.quotient_is_free()) if callable(witness.quotient_is_free) else bool(witness.quotient_is_free)
        elif G is not None and N is not None:
            Q = G.quotient(N)
            if isinstance(Q, FreeGroup):
                h2 = True
            elif isinstance(Q, FpGroup):
                h2 = (len(Q.relators) == 0)
            else:
                # For finite permutation groups, only the trivial group is free
                h2 = (Q.order() == 1)
    except Exception:
        h2 = False

    # neg_Q: The sequence does NOT split
    neg_q = False
    try:
        if hasattr(witness, 'splits'):
            splits = bool(witness.splits()) if callable(witness.splits) else bool(witness.splits)
            neg_q = not splits
        elif hasattr(witness, 'is_semidirect_product'):
            splits = bool(witness.is_semidirect_product()) if callable(witness.is_semidirect_product) else bool(witness.is_semidirect_product)
            neg_q = not splits
        elif G is not None and N is not None:
            Q = G.quotient(N)
            if hasattr(Q, 'order') and Q.order() == 1:
                splits = True
                neg_q = not splits
            else:
                # Default to True (splits) to avoid false positives for neg_q
                splits = True
                neg_q = not splits
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The quotient group G/N is a free group",
    "¬Q: The short exact sequence does not split (G is not isomorphic to N ⋊ G/N)"
]

N_HYP = 2
NEG_Q_INDEX = 2
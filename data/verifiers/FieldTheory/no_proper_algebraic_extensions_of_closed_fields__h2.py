import sympy
from sympy import CC, RR, QQ
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and fails the conclusion.
    The witness should be a tuple (K, L) representing the base field K and the extension L.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        K, L = witness
    except Exception:
        return [False, False, False]

    # H1: K is an algebraically closed field
    try:
        # In SymPy, CC is the standard algebraically closed field.
        h1 = (K == CC) or (str(K) == 'CC') or (str(K) == 'Complexes')
    except Exception:
        h1 = False

    # H2: L is an algebraic extension of K
    try:
        h2 = False
        if L == K or str(L) == str(K):
            h2 = True
        elif hasattr(L, 'ring') and hasattr(L, 'base_ideal'):
            # L is a quotient ring K[x]/I
            ring_domain = getattr(L.ring, 'domain', None)
            if ring_domain == K or str(ring_domain) == str(K):
                if len(getattr(L.ring, 'gens', [])) == 1:
                    try:
                        gens = L.base_ideal.gens
                        # If the ideal is non-zero, the quotient is finite-dimensional, hence algebraic
                        if gens and not all(g == 0 for g in gens):
                            h2 = True
                    except Exception:
                        pass
        elif hasattr(L, 'domain'):
            # L is an AlgebraicField extension
            if L.domain == K or str(L.domain) == str(K):
                if hasattr(L, 'ext'):
                    h2 = True
        elif str(K) == 'RR' and str(L) == 'CC':
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: L is not equal to K
    try:
        neg_q = (L != K) and (str(L) != str(K))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: L is an algebraic extension of K",
    "¬Q: L is not equal to K"
]

N_HYP = 2
NEG_Q_INDEX = 2
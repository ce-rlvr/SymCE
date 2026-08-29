import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    witness is expected to be a tuple: (R, G, u, v)
    where:
      - R is a sympy Domain (e.g., sympy.ZZ) representing the integral domain.
      - G is a sympy PermutationGroup.
      - u and v are dictionaries mapping Permutation objects to coefficients in R,
        representing elements in the group ring RG.
    """
    try:
        R, G, u, v = witness
    except Exception:
        return [False, False, False]

    # H_1: R is an integral domain
    try:
        h1_ok = False
        if R in [sympy.ZZ, sympy.QQ]:
            h1_ok = True
        elif hasattr(R, 'is_Domain') and R.is_Domain:
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: RG is the group ring of G over R (u and v are valid elements in RG)
    try:
        def is_in_RG(w):
            if not isinstance(w, dict):
                return False
            for g, c in w.items():
                if not isinstance(g, Permutation):
                    return False
                if g not in G:
                    return False
                if c not in R:
                    return False
            return True

        h2_ok = isinstance(G, PermutationGroup) and is_in_RG(u) and is_in_RG(v)
    except Exception:
        h2_ok = False

    # ¬Q: The group of units of RG does NOT consist exactly of the elements of the form c*g.
    # This means there exists a unit in RG (witnessed by u, with inverse v) that is not of the form c*g.
    try:
        def group_ring_mult(w1, w2):
            res = {}
            for g1, c1 in w1.items():
                for g2, c2 in w2.items():
                    g = g1 * g2
                    res[g] = res.get(g, 0) + c1 * c2
            return {g: c for g, c in res.items() if c != 0}

        uv = group_ring_mult(u, v)
        vu = group_ring_mult(v, u)

        def is_id(w):
            w_clean = {g: c for g, c in w.items() if c != 0}
            if len(w_clean) != 1:
                return False
            return w_clean.get(G.identity, 0) == 1

        is_unit = is_id(uv) and is_id(vu)

        # An element is of the form c*g iff it has exactly one non-zero term.
        u_clean = {g: c for g, c in u.items() if c != 0}
        not_trivial_form = len(u_clean) > 1

        neg_q_ok = is_unit and not_trivial_form
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: RG is the group ring of G over R and u, v in RG",
    "not Q: There exists a unit in RG that is not of the form c*g"
]

N_HYP = 2
NEG_Q_INDEX = 2
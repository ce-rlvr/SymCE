import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Q = sympy.S.Rationals
R = sympy.S.Reals
C = sympy.S.Complexes
Z = sympy.S.Integers

def is_elementary_abelian_p_group(witness):
    try:
        if hasattr(witness, 'is_abelian') and not witness.is_abelian:
            return False
        if hasattr(witness, 'elements'):
            elements = list(witness.elements)
            if len(elements) <= 1:
                return False
            orders = set(e.order() for e in elements if e.order() > 1)
            if len(orders) == 1:
                p = orders.pop()
                if sympy.isprime(p):
                    return True
            return False
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    # H1: G contains at least two elements
    h1 = False
    try:
        if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, sympy.S.Integers):
            h1 = True
        elif hasattr(witness, 'order'):
            h1 = witness.order() >= 2
        elif isinstance(witness, str) and witness.lower() in ['q', 'r', 'c', 'rationals', 'reals', 'complexes', 'z', 'integers']:
            h1 = True
    except Exception:
        pass

    # H2: Aut(G) is transitive on G \ {1}
    # Note: For finite groups, Aut(G) is transitive on G \ {1} if and only if G is an elementary abelian p-group.
    h2 = False
    try:
        if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h2 = True
        elif witness == sympy.S.Integers:
            h2 = False
        elif isinstance(witness, str):
            w_lower = witness.lower()
            if w_lower in ['q', 'r', 'c', 'rationals', 'reals', 'complexes']:
                h2 = True
            elif w_lower in ['z', 'integers']:
                h2 = False
        elif hasattr(witness, 'order') and hasattr(witness, 'elements'):
            h2 = is_elementary_abelian_p_group(witness)
    except Exception:
        pass

    # neg_Q: G is NOT an elementary abelian p-group
    neg_q = False
    try:
        if witness in (sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes, sympy.S.Integers):
            neg_q = True
        elif isinstance(witness, str):
            neg_q = True
        elif hasattr(witness, 'order') and hasattr(witness, 'elements'):
            neg_q = not is_elementary_abelian_p_group(witness)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G contains at least two elements",
    "H_2: Aut(G) acts transitively on non-identity elements",
    "¬Q: G is not an elementary abelian p-group"
]

N_HYP = 2
NEG_Q_INDEX = 2
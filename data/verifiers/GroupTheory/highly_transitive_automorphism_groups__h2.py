import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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

def is_elementary_abelian(witness):
    try:
        is_ab = getattr(witness, 'is_abelian', False)
        if callable(is_ab):
            is_ab = is_ab()
        if not is_ab:
            return False
        
        elems = witness.elements
        if callable(elems):
            elems = elems()
        elements = list(elems)
        
        non_id = [g for g in elements if int(g.order()) > 1]
        if not non_id:
            return False
            
        orders = set(int(g.order()) for g in non_id)
        if len(orders) == 1:
            p = list(orders)[0]
            if isprime(p):
                return True
        return False
    except Exception:
        return False

def conditions(witness):
    # H1: G is a finite group
    try:
        h1 = False
        if hasattr(witness, 'order') and hasattr(witness, 'elements'):
            o = int(witness.order())
            if o > 0:
                h1 = True
    except Exception:
        h1 = False

    # H2: For any two non-identity elements x, y \in G, there exists an automorphism \alpha \in Aut(G) such that \alpha(x) = y
    # Mathematically, for finite groups, Aut(G) acts transitively on G \ {1} if and only if 
    # G is an elementary abelian p-group or G is the trivial group.
    try:
        h2 = False
        if h1:
            o = int(witness.order())
            if o == 1:
                h2 = True
            else:
                h2 = is_elementary_abelian(witness)
    except Exception:
        h2 = False

    # neg_Q: G is NOT an elementary abelian p-group for some prime p
    try:
        neg_q = False
        if h1:
            neg_q = not is_elementary_abelian(witness)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: For any two non-identity elements x, y in G, there exists an automorphism mapping x to y",
    "¬Q: G is not an elementary abelian p-group for some prime p"
]

N_HYP = 2
NEG_Q_INDEX = 2
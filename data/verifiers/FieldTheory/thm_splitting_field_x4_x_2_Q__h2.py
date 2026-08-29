import sympy
from sympy import Symbol
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

x = Symbol('x')

def conditions(witness):
    h1 = True
    neg_q = False

    try:
        if isinstance(witness, dict) and 'f' in witness:
            f_val = witness['f']
            if sympy.simplify(f_val - (x**4 + x + 2)) != 0:
                h1 = False
    except Exception:
        h1 = False

    try:
        deg = None
        grp = None
        if isinstance(witness, dict):
            deg = witness.get('degree', None)
            grp = witness.get('group', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            deg, grp = witness
        
        q_holds = False
        if deg == 24:
            if grp is not None and hasattr(grp, 'is_isomorphic'):
                if grp.is_isomorphic(S4):
                    q_holds = True
                    
        neg_q = not q_holds
    except Exception:
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Let f(x) = x**4 + x + 2 in Q",
    "not Q: The degree of the extension K over Q is not 24, or the Galois group of K over Q is not isomorphic to S4"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.abc import x

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
S5 = SymmetricGroup(5)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

f_target = x**5 - 4*x + 2

def conditions(witness):
    f = f_target
    G = None
    d = None
    
    if isinstance(witness, dict):
        f = witness.get('f', f_target)
        G = witness.get('G', witness.get('galois_group', None))
        d = witness.get('d', witness.get('degree', None))
    elif isinstance(witness, (tuple, list)):
        if len(witness) == 3:
            f, G, d = witness
        elif len(witness) == 2:
            G, d = witness
    else:
        G = getattr(witness, 'G', getattr(witness, 'galois_group', None))
        d = getattr(witness, 'd', getattr(witness, 'degree', None))
        
    if G is not None and d is None:
        try:
            d = G.order()
        except Exception:
            pass

    try:
        if f == f_target:
            h1 = True
        else:
            h1 = bool(sympy.simplify(f - f_target) == 0)
    except Exception:
        h1 = False
        
    try:
        if G is None or d is None:
            neg_q = False
        else:
            is_S5 = (G.order() == 120) and G.is_isomorphic(S5)
            is_deg_120 = (d == 120)
            neg_q = not (is_S5 and is_deg_120)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = ['H_1: f is x^5 - 4x + 2', 'not Q: Gal is not S5 or degree is not 120']

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness):
    def eval_attr(obj, *attr_names):
        for attr_name in attr_names:
            if hasattr(obj, attr_name):
                attr = getattr(obj, attr_name)
                return bool(attr() if callable(attr) else attr)
        return None

    # H1: G is finitely generated
    h1 = False
    try:
        val = eval_attr(witness, 'is_finitely_generated', 'is_finitely_generated_group')
        if val is not None:
            h1 = val
        elif hasattr(witness, 'generators'):
            h1 = len(list(witness.generators)) < float('inf')
    except Exception:
        pass

    # H2: Every element of G has finite order
    h2 = False
    try:
        val = eval_attr(witness, 'is_torsion', 'is_torsion_group')
        if val is not None:
            h2 = val
        else:
            is_fin = eval_attr(witness, 'is_finite', 'is_finite_group')
            if is_fin is None and hasattr(witness, 'order'):
                try:
                    o = witness.order()
                    if callable(o): o = o()
                    if o != sympy.oo and o != sympy.S.Infinity:
                        is_fin = True
                except Exception:
                    pass
            
            if is_fin:
                h2 = True
            elif hasattr(witness, 'elements'):
                h2 = True
                count = 0
                for g in witness.elements:
                    if hasattr(g, 'order'):
                        o = g.order()
                        if callable(o): o = o()
                        if o == sympy.oo or o == sympy.S.Infinity:
                            h2 = False
                            break
                    count += 1
                    if count > 200:
                        break
    except Exception:
        pass

    # neg_Q: G is not finite
    neg_q = False
    try:
        val = eval_attr(witness, 'is_finite', 'is_finite_group')
        if val is not None:
            neg_q = not val
        elif hasattr(witness, 'order'):
            try:
                o = witness.order()
                if callable(o): o = o()
                if o == sympy.oo or o == sympy.S.Infinity:
                    neg_q = True
            except Exception:
                pass
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is finitely generated",
    "H_2: Every element of G has finite order",
    "¬Q: G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import S, FiniteSet, oo

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
    h1, h2, neg_q = False, False, False
    try:
        # Extract kernel, image, and domain from the witness
        if isinstance(witness, dict):
            ker = witness.get('kernel', witness.get('ker'))
            img = witness.get('image', witness.get('im'))
            dom = witness.get('domain', witness.get('G'))
        elif isinstance(witness, tuple) and len(witness) == 3:
            ker, img, dom = witness
        else:
            ker = getattr(witness, 'kernel', getattr(witness, 'ker', None))
            img = getattr(witness, 'image', getattr(witness, 'im', None))
            dom = getattr(witness, 'domain', getattr(witness, 'G', None))

        def is_finite(obj):
            if obj is None:
                return False
            if isinstance(obj, (int, sympy.Integer)):
                return True
            if obj == oo:
                return False
            if hasattr(obj, 'is_finite') and obj.is_finite is not None:
                return bool(obj.is_finite)
            if hasattr(obj, 'order'):
                try:
                    ord_val = obj.order()
                    if ord_val == oo:
                        return False
                    return True
                except Exception:
                    pass
            if hasattr(obj, '__len__'):
                return True
            if isinstance(obj, bool):
                return obj
            return False

        def is_infinite(obj):
            if obj is None:
                return False
            if obj == oo:
                return True
            if isinstance(obj, (int, sympy.Integer)):
                return False
            if hasattr(obj, 'is_finite') and obj.is_finite is not None:
                return not bool(obj.is_finite)
            if hasattr(obj, 'order'):
                try:
                    ord_val = obj.order()
                    if ord_val == oo:
                        return True
                    return False
                except Exception:
                    pass
            if isinstance(obj, str) and obj.lower() == 'infinite':
                return True
            return False

        h1 = is_finite(ker)
        h2 = is_finite(img)
        neg_q = is_infinite(dom)

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Kernel ker(f) is a finite group",
    "H_2: Image f(G) is a finite group",
    "¬Q: Domain group G is not a finite group"
]

N_HYP = 2
NEG_Q_INDEX = 2
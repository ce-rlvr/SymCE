import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    n = None
    W = None
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            W = witness.get('W')
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                n, W = witness
            elif len(witness) == 1:
                n = witness[0]
                W = None
        elif hasattr(witness, 'n'):
            n = witness.n
            W = getattr(witness, 'W', None)
        else:
            n = witness
            W = None
    except Exception:
        pass

    # H_1: Let n >= 2 be an integer.
    try:
        if float(n) == int(n):
            h1 = (int(n) >= 2)
        else:
            h1 = False
    except Exception:
        h1 = False

    # neg_Q: W does NOT admit the presentation of the affine Coxeter group A-tilde_n
    try:
        if W is None:
            neg_q = False
        else:
            is_presented_group = False
            try:
                from sympy.combinatorics.fp_groups import FpGroup
                # If W is an FpGroup with exactly n+1 generators, we conservatively assume 
                # it might be the presented affine Coxeter group.
                if isinstance(W, FpGroup):
                    if len(W.generators) == int(n) + 1:
                        is_presented_group = True
            except Exception:
                pass
            
            # Any finite group (like S3, Z2) or other object provided as a counterexample 
            # does not admit the presentation of the infinite affine Coxeter group.
            if is_presented_group:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 2 is an integer",
    "¬Q: W does not admit the presentation of the affine Coxeter group A-tilde_n"
]

N_HYP = 1
NEG_Q_INDEX = 1
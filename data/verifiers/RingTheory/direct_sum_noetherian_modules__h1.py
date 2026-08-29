import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, oo

# Top-level setup for potential witness elements
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
    """
    Evaluates the hypotheses and the negated conclusion for the conjecture:
    H1: n is a positive integer
    H2: M_1, M_2, ..., M_n are Noetherian R-modules
    Q: The finite direct sum is a Noetherian R-module
    
    The witness is expected to be a list of modules (represented by their dimensions, 
    orders, or as sympy objects), or a tuple (n, [M_1, ..., M_n]).
    """
    # Parse witness
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, modules = witness
        else:
            modules = witness
            n = len(modules) if isinstance(modules, (list, tuple)) else 0
    except Exception:
        modules = []
        n = 0

    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0 and isinstance(modules, (list, tuple)) and len(modules) == n
    except Exception:
        h1 = False

    def is_noeth(m):
        if m == oo:
            return False
        if isinstance(m, (int, float)):
            return True
        if hasattr(m, 'is_Integer') and m.is_Integer:
            return True
        if hasattr(m, 'order'):
            try:
                return m.order() < oo
            except Exception:
                pass
        if hasattr(m, 'shape'):
            return True
        return False

    # H_2: M_1, M_2, \dots, M_n are Noetherian R-modules
    try:
        if isinstance(modules, (list, tuple)):
            h2 = all(is_noeth(m) for m in modules)
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: The finite direct sum \bigoplus_{i=1}^n M_i is not a Noetherian R-module
    # A finite direct sum of modules is Noetherian if and only if each component is Noetherian.
    try:
        if isinstance(modules, (list, tuple)):
            neg_q = not all(is_noeth(m) for m in modules)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    r"H_1: n is a positive integer",
    r"H_2: M_1, M_2, \dots, M_n are Noetherian R-modules",
    r"¬Q: The finite direct sum \bigoplus_{i=1}^n M_i is not a Noetherian R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
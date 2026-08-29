import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.ntheory import factorint

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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    Since the hypothesis defining C was dropped, C is a free variable.
    The witness is expected to be a tuple (G, C).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, C = witness
        else:
            G = witness
            C = None
    except Exception:
        return [False, False]

    # H_1: G is a finite non-abelian simple group
    h1_ok = False
    try:
        if isinstance(G, PermutationGroup) and getattr(G, 'is_abelian', None) is False:
            is_simple = False
            if hasattr(G, 'is_simple'):
                val = G.is_simple
                if callable(val):
                    val = val()
                if val is not None:
                    is_simple = val
                else:
                    ns = G.normal_subgroups()
                    is_simple = (len(ns) == 2)
            else:
                if hasattr(G, 'normal_subgroups'):
                    ns = G.normal_subgroups()
                    is_simple = (len(ns) == 2)
            
            if is_simple:
                h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The size of C is of the form p^k for some prime p and integer k >= 1
    neg_q_ok = False
    try:
        if C is not None:
            size_C = None
            if hasattr(C, '__len__'):
                size_C = len(C)
            else:
                for attr in ['order', 'size']:
                    if hasattr(C, attr):
                        val = getattr(C, attr)
                        if callable(val):
                            try:
                                size_C = val()
                            except Exception:
                                pass
                        else:
                            size_C = val
                        if size_C is not None:
                            break
            
            if size_C is not None:
                try:
                    size_C = int(size_C)
                    if size_C >= 2:
                        factors = factorint(size_C)
                        if len(factors) == 1:
                            neg_q_ok = True
                except Exception:
                    pass
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite non-abelian simple group",
    "¬Q: The size of C is of the form p^k for some prime p and integer k >= 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
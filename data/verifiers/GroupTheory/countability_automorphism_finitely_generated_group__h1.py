import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a counterexample to the false conjecture:
    "The automorphism group Aut(G) is a countable group"
    (The dropped hypothesis was that G is finitely generated).
    """
    neg_q = False
    try:
        from sympy import S
        if witness in (S.Reals, S.Complexes):
            neg_q = True
        elif witness in (S.Rationals, S.Integers):
            neg_q = False
        elif isinstance(witness, str):
            s = witness.lower()
            if s in ('r', 'c', 'reals', 'complexes', 'r^n', 'c^n'):
                neg_q = True
            elif 'oo' in s or 'infinity' in s or 'aleph' in s:
                neg_q = True
            elif 'z' in s and ('^' in s or '**' in s):
                neg_q = True
            elif 'q' in s and ('^' in s or '**' in s):
                neg_q = True
            elif 'prod' in s or 'direct sum' in s or 'oplus' in s or 'otimes' in s:
                neg_q = True
        else:
            from sympy.combinatorics import PermutationGroup, FpGroup, FreeGroup
            if isinstance(witness, (PermutationGroup, FpGroup, FreeGroup)):
                neg_q = False
            elif hasattr(witness, 'is_finitely_generated') and witness.is_finitely_generated:
                neg_q = False
            elif hasattr(witness, 'automorphism_group_is_countable'):
                val = witness.automorphism_group_is_countable
                if callable(val):
                    neg_q = not bool(val())
                else:
                    neg_q = not bool(val)
            else:
                name = getattr(type(witness), '__name__', '')
                if 'Infinite' in name or 'Uncountable' in name or 'Product' in name:
                    neg_q = True
    except Exception:
        pass
        
    return [neg_q]

CONDITION_LABELS = ["¬Q: Aut(G) is not a countable group"]
N_HYP = 0
NEG_Q_INDEX = 0
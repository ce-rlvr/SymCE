import sympy
import sympy.abc
import math
import itertools
import functools

class FieldExtension:
    """
    Represents a field extension K/F for the purpose of verifying this conjecture.
    Since SymPy does not natively represent infinite algebraic extensions, we use 
    this mock object to evaluate the properties of the extension.
    """
    def __init__(self, name, is_normal, is_finite):
        self.name = name
        self.is_normal = is_normal
        self.is_finite = is_finite

    def __str__(self):
        return self.name

# Top-level setup: named object bindings that the witness expression may reference.
# A counterexample must be an infinite normal extension.
Q_alg = FieldExtension("Algebraic closure of Q", is_normal=True, is_finite=False)
Q_sqrt_primes = FieldExtension("Q adjoin sqrt of all primes", is_normal=True, is_finite=False)

# Standard non-counterexamples (finite extensions)
Q_cbrt_2 = FieldExtension("Q(cbrt(2))", is_normal=False, is_finite=True)
Q_i = FieldExtension("Q(i)", is_normal=True, is_finite=True)


def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'is_normal') and hasattr(witness, 'is_finite'):
            is_normal = bool(witness.is_normal)
            is_finite = bool(witness.is_finite)
        elif isinstance(witness, str):
            # Fallback for string-based witnesses
            if witness in ["Q_alg", "Q_sqrt_primes", "AlgebraicClosure(QQ)"]:
                is_normal = True
                is_finite = False
            else:
                return [False]
        else:
            # Any standard SymPy AlgebraicField is a finite extension.
            # Finite extensions cannot be counterexamples to this conjecture.
            return [False]
            
        # A field extension is the splitting field of a single polynomial f(x) in F[x]
        # if and only if it is a FINITE and NORMAL extension.
        is_splitting_field = is_finite and is_normal
        
        # The conjecture claims: K/F is normal iff K is the splitting field of some polynomial
        conclusion = (is_normal == is_splitting_field)
        
        # The negated conclusion is True when the equivalence fails
        neg_q = not conclusion
        
    except Exception:
        neg_q = False

    return [neg_q]


CONDITION_LABELS = [
    "¬Q: K/F is a normal extension but not the splitting field of a single polynomial (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0
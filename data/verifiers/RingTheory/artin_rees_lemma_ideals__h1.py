import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    # H_1: I and J are ideals of R
    h1 = False
    try:
        if hasattr(witness, 'I_is_ideal') and hasattr(witness, 'J_is_ideal'):
            h1 = bool(witness.I_is_ideal and witness.J_is_ideal)
        elif hasattr(witness, 'is_ideal_I') and hasattr(witness, 'is_ideal_J'):
            h1 = bool(witness.is_ideal_I() and witness.is_ideal_J())
        elif hasattr(witness, 'I') and hasattr(witness, 'J'):
            I_ideal = witness.I.is_ideal() if callable(getattr(witness.I, 'is_ideal', None)) else getattr(witness.I, 'is_ideal', True)
            J_ideal = witness.J.is_ideal() if callable(getattr(witness.J, 'is_ideal', None)) else getattr(witness.J, 'is_ideal', True)
            h1 = bool(I_ideal and J_ideal)
        elif isinstance(witness, dict):
            if 'I_is_ideal' in witness and 'J_is_ideal' in witness:
                h1 = bool(witness['I_is_ideal'] and witness['J_is_ideal'])
            elif 'I' in witness and 'J' in witness:
                I = witness['I']
                J = witness['J']
                I_ideal = I.is_ideal() if callable(getattr(I, 'is_ideal', None)) else getattr(I, 'is_ideal', True)
                J_ideal = J.is_ideal() if callable(getattr(J, 'is_ideal', None)) else getattr(J, 'is_ideal', True)
                h1 = bool(I_ideal and J_ideal)
            else:
                h1 = bool(witness.get('is_ideal', True))
    except Exception:
        h1 = False

    # neg_Q: For all c >= 1, there exists n >= c such that I^n \cap J != I^{n-c}(I^c \cap J)
    neg_q = False
    try:
        neg_q_holds = True
        
        def check_eq(c, n):
            if hasattr(witness, 'artin_rees_eq'):
                return bool(witness.artin_rees_eq(c, n))
            if isinstance(witness, dict) and 'artin_rees_eq' in witness:
                return bool(witness['artin_rees_eq'](c, n))
            
            if hasattr(witness, 'I') and hasattr(witness, 'J'):
                I = witness.I
                J = witness.J
            elif isinstance(witness, dict) and 'I' in witness and 'J' in witness:
                I = witness['I']
                J = witness['J']
            else:
                raise ValueError("No way to check equality")
                
            left = (I ** n) & J
            right = (I ** (n - c)) * ((I ** c) & J)
            return bool(left == right)

        # We check for c in 1..5. If for all these c, we find an n in c+1..c+14 where equality fails, neg_q is True.
        # (Note: for n = c, the equality trivially holds as I^0 = R, so we search n > c)
        for c in range(1, 6):
            found_n = False
            for n in range(c + 1, c + 15):
                if not check_eq(c, n):
                    found_n = True
                    break
            if not found_n:
                neg_q_holds = False
                break
                
        neg_q = neg_q_holds
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are ideals of R",
    "¬Q: For all c >= 1, there exists n >= c such that I^n \\cap J != I^{n-c}(I^c \\cap J)"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.abc import x, y, z
from sympy import Rational, Integer
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    Returns [H1_ok, neg_Q_ok].
    """
    if callable(witness):
        try:
            res = witness()
            if isinstance(res, (list, tuple)) and len(res) == 2:
                return [bool(res[0]), bool(res[1])]
        except Exception:
            pass

    H1 = False
    neg_Q = False
    
    R, I, J = None, None, None
    
    # 1. Evaluate Hypothesis H1: R is a commutative Noetherian ring
    try:
        if hasattr(witness, 'is_commutative_Noetherian'):
            H1 = bool(witness.is_commutative_Noetherian())
        elif hasattr(witness, 'H1'):
            H1 = bool(witness.H1())
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
            if hasattr(R, 'is_commutative'):
                H1 = bool(R.is_commutative)
            else:
                H1 = True
        elif isinstance(witness, dict) and 'R' in witness:
            R = witness['R']
            I = witness.get('I')
            J = witness.get('J')
            if hasattr(R, 'is_commutative'):
                H1 = bool(R.is_commutative)
            else:
                H1 = True
        elif hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J'):
            R = witness.R
            I = witness.I
            J = witness.J
            if hasattr(R, 'is_commutative'):
                H1 = bool(R.is_commutative)
            else:
                H1 = True
    except Exception:
        pass

    # 2. Evaluate Negated Conclusion neg_Q:
    # For all c >= 1, there exists n >= c such that I^n \cap J != I^{n-c}(I^c \cap J)
    try:
        if hasattr(witness, 'check_conclusion'):
            neg_Q = not bool(witness.check_conclusion())
        elif hasattr(witness, 'equation_holds'):
            neg_Q_eval = True
            for c in range(1, 6):
                c_works = True
                for n in range(c + 1, c + 6):
                    if not witness.equation_holds(c, n):
                        c_works = False
                        break
                if c_works:
                    neg_Q_eval = False
                    break
            neg_Q = neg_Q_eval
        elif I is not None and J is not None:
            neg_Q_eval = True
            for c in range(1, 6):
                c_works = True
                for n in range(c + 1, c + 6):
                    computed = False
                    try:
                        # Try standard python/sympy operators
                        I_n = I**n
                        I_c = I**c
                        I_n_minus_c = I**(n-c)
                        lhs = I_n.intersect(J)
                        rhs = I_n_minus_c * (I_c.intersect(J))
                        computed = True
                    except Exception:
                        pass
                    
                    if not computed:
                        try:
                            # Try custom method names
                            lhs = I.power(n).intersect(J)
                            rhs = I.power(n-c).mult(I.power(c).intersect(J))
                            computed = True
                        except Exception:
                            pass
                            
                    if not computed:
                        # If we cannot compute the operations, we cannot verify the counterexample
                        return [H1, False]
                        
                    if lhs != rhs:
                        c_works = False
                        break
                if c_works:
                    # Found a 'c' where the equation holds for all tested 'n'
                    neg_Q_eval = False
                    break
            neg_Q = neg_Q_eval
    except Exception:
        pass

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: For all c >= 1, there exists n >= c such that I^n \\cap J != I^{n-c}(I^c \\cap J)"
]

N_HYP = 1
NEG_Q_INDEX = 1
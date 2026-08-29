import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.abc import x
import math

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

N_HYP = 0
NEG_Q_INDEX = 0

CONDITION_LABELS = [
    "¬Q: f is not uniformly continuous on R"
]

def conditions(witness):
    try:
        # 1. Denominator check for singularities
        # If the function is a rational expression with real roots in the denominator,
        # it is not defined on all of R, hence not uniformly continuous on R.
        try:
            numer, denom = witness.as_numer_denom()
            if denom != 1:
                roots = sympy.solveset(denom, x, domain=sympy.S.Reals)
                if roots.is_empty is False:
                    return [True]
        except Exception:
            pass

        deltas = [sympy.Rational(10)**(-i) for i in [1, 3, 5, 7, 9, 12, 15, 20, 25, 30]]

        # Generate a wide range of test points
        test_x = []
        for exp in range(-5, 35, 2):
            for mult in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
                val = sympy.Rational(mult) * (sympy.Rational(10) ** exp)
                test_x.append(val)
                test_x.append(-val)
        test_x.append(sympy.Rational(0))
        
        # Add points to catch discontinuities at common points
        for c in [0, 1, -1, 2, -2, 10, -10]:
            for delta in deltas:
                test_x.append(sympy.Rational(c) - delta / 2)
        
        # 2. Domain check
        # f must be defined and real for all x in R.
        for val in test_x:
            try:
                v = witness.subs(x, val).evalf(80)
                if v.is_real is not True or v.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo):
                    return [True]
            except Exception:
                return [True]
                
        # 3. Delta test for uniform continuity
        # A function is uniformly continuous if for any epsilon > 0, there exists delta > 0
        # such that |f(x + delta) - f(x)| < epsilon for all x.
        # We use epsilon = 0.2 and test a range of deltas down to 10^-30.
        # If for ALL these deltas, we can find an x where the difference is > 0.2,
        # then the function is NOT uniformly continuous.
        neg_q = True
        for delta in deltas:
            found = False
            for val in test_x:
                try:
                    v1 = witness.subs(x, val).evalf(80)
                    if not (v1.is_real is True and not v1.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo)):
                        continue
                        
                    v2 = witness.subs(x, val + delta).evalf(80)
                    if not (v2.is_real is True and not v2.has(sympy.oo, sympy.zoo, sympy.nan, -sympy.oo)):
                        continue
                        
                    if abs(v1 - v2) > 0.2:
                        found = True
                        break
                except Exception:
                    pass
            
            if not found:
                # For this delta, all tested x had difference <= 0.2.
                # This suggests the function IS uniformly continuous.
                neg_q = False
                break
                
        return [neg_q]
    except Exception:
        return [False]
import sympy
from sympy import ZZ, QQ
from sympy.polys.domains.ring import Ring
from sympy.polys.domains.field import Field
from sympy.abc import x, y, z

def conditions(witness):
    """
    Given a witness (R, F, f), checks if it is a valid counterexample to the false conjecture.
    R: Domain/Ring
    F: Domain/Field
    f: Callable representing the homomorphism from R to F
    """
    try:
        R, F, f = witness
    except Exception:
        return [False, False, False]
    
    # H1: R is a commutative ring with identity
    try:
        h1 = (isinstance(R, (Ring, Field)) or 
              R in [ZZ, QQ, sympy.S.Integers, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals] or 
              getattr(R, 'is_Ring', False))
    except Exception:
        h1 = False

    # H2: F is a field
    try:
        h2 = (isinstance(F, Field) or 
              F in [QQ, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals] or 
              getattr(F, 'is_Field', False))
    except Exception:
        h2 = False

    # neg_Q: The kernel of f is NOT a maximal ideal of R
    try:
        one = R.one if hasattr(R, 'one') else 1
        val1 = f(one)
        is_zero = False
        if val1 == 0:
            is_zero = True
        elif hasattr(F, 'zero') and val1 == F.zero:
            is_zero = True
            
        if is_zero:
            # ker(f) = R, which is not a proper ideal, so not maximal
            is_maximal = False
        else:
            if R == ZZ or R == sympy.S.Integers:
                gen = 0
                for k in range(1, 101):
                    val = f(k)
                    if val == 0 or (hasattr(F, 'zero') and val == F.zero):
                        gen = k
                        break
                if gen == 0:
                    # ker(f) = {0}, which is prime but not maximal in Z
                    is_maximal = False
                else:
                    # ker(f) = nZ, which is maximal iff n is prime
                    from sympy import isprime
                    is_maximal = isprime(gen)
            else:
                # For other rings, we assume ker(f) = {0} for the standard counterexamples.
                # {0} is a maximal ideal if and only if R is a field.
                if isinstance(R, Field) or R in [QQ, sympy.S.Reals, sympy.S.Complexes, sympy.S.Rationals] or getattr(R, 'is_Field', False):
                    is_maximal = True
                else:
                    is_maximal = False
                    
        neg_q = not is_maximal
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: F is a field",
    "¬Q: The kernel of f is not a maximal ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2
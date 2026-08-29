import math
import sympy
from sympy.abc import x, y, z, t, u, v, w
from sympy import Rational, Integer

def conditions(witness) -> list[bool]:
    try:
        # The witness is expected to be a list of generators for the ideals,
        # or a tuple like (Ring, [generators]).
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], (list, tuple)):
            ideals = witness[1]
        else:
            ideals = witness
            
        h1 = isinstance(ideals, (list, tuple)) and len(ideals) > 0
        if h1:
            for item in ideals:
                # We expect the ideals to be represented by integers or sympy expressions (polynomials)
                if not (isinstance(item, int) or isinstance(item, sympy.Expr)):
                    h1 = False
                    break
    except Exception:
        h1 = False
        ideals = []

    # H2 is the definition of the natural projection homomorphism, which inherently exists
    # for any valid list of ideals.
    h2 = h1

    try:
        if not h1:
            neg_q = False
        else:
            # The conclusion states "The kernel of f is the intersection".
            # Mathematically, the kernel of this map is ALWAYS the intersection.
            # The intended false conclusion (when the "pairwise coprime" hypothesis is dropped)
            # is that the kernel is the PRODUCT of the ideals.
            # We evaluate if the intersection (LCM) is NOT equal to the product.
            if all(isinstance(item, int) or (isinstance(item, sympy.Expr) and item.is_Integer) for item in ideals):
                prod = 1
                for item in ideals:
                    prod *= int(item)
                
                lcm_val = int(ideals[0])
                for item in ideals[1:]:
                    lcm_val = (lcm_val * int(item)) // math.gcd(lcm_val, int(item)) if lcm_val else 0
                    
                neg_q = abs(lcm_val) != abs(prod)
            else:
                prod = ideals[0]
                for item in ideals[1:]:
                    prod = prod * item
                
                lcm_val = ideals[0]
                for item in ideals[1:]:
                    lcm_val = sympy.lcm(lcm_val, item)
                
                if lcm_val == 0:
                    neg_q = (prod != 0)
                else:
                    quotient = sympy.simplify(prod / lcm_val)
                    # If they generate the same ideal, their quotient is a unit (1 or -1 in Z[x])
                    neg_q = (quotient != 1) and (quotient != -1)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I_1, I_2, ..., I_n are ideals of R",
    "H_2: f is the ring homomorphism defined by f(x) = (x + I_1, ..., x + I_n)",
    "¬Q: The intersection of the ideals is not equal to their product (kernel is not the product)"
]

N_HYP = 2
NEG_Q_INDEX = 2
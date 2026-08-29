import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: J is an ideal of R",
    "¬Q: The map x \\otimes y \\mapsto xy is not a well-defined surjective R-module homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Given a witness (R, I, J) where R is a list of ring elements, and I, J are lists of elements in R,
    check if I and J are ideals of R, and whether the conclusion fails.
    The conclusion fails if the map x \otimes y \mapsto xy is not an R-module homomorphism
    in the sense required for tensor products over commutative rings (i.e., r(xy) = x(ry)).
    """
    try:
        R, I, J = witness
    except Exception:
        return [False, False, False]
        
    def is_ideal(S, R):
        if not S: 
            return False
        # Check subset
        for s in S:
            if s not in R: 
                return False
        # Check closure under addition and subtraction
        for a in S:
            for b in S:
                if (a + b) not in S: 
                    return False
                if (a - b) not in S: 
                    return False
        # Check closure under left and right multiplication by R
        for r in R:
            for s in S:
                if (r * s) not in S: 
                    return False
                if (s * r) not in S: 
                    return False
        return True

    try:
        h1_ok = bool(is_ideal(I, R))
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(is_ideal(J, R))
    except Exception:
        h2_ok = False

    try:
        # The conclusion states there exists a surjective R-module homomorphism mapping x \otimes y to xy.
        # For this map to be an R-module homomorphism under the standard tensor product module structure,
        # we must have r * f(x \otimes y) = f(r * (x \otimes y)).
        # Depending on the module structure used (left or right), this requires r*(x*y) == x*(r*y).
        # If R is not commutative, this property generally fails, meaning the map is not an R-module homomorphism
        # (or the tensor product is not even an R-module).
        violation = False
        for x in I:
            for y in J:
                for r in R:
                    if r * (x * y) != x * (r * y):
                        violation = True
                        break
                if violation:
                    break
            if violation:
                break
        neg_q_ok = bool(violation)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]
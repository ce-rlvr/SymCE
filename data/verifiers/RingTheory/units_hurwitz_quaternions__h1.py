import sympy
from sympy import Matrix, eye, zeros, Rational, Integer

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The conjecture claims that for u in H, u is a unit iff its norm is 1, 
    and the units of H form the binary tetrahedral group.
    
    The false conjecture arises from dropping the hypothesis that u is a Hurwitz integer.
    Without it, u is just a real quaternion (in Lean, H = real quaternions).
    In the real quaternions, every non-zero element is a unit, so "u is a unit iff norm is 1" is false.
    """
    try:
        # H_1: Let u \in H (real quaternions)
        # We accept numbers, tuples of length 4, sympy Quaternions, or 2x2 complex matrices
        if hasattr(witness, 'det'):
            norm_sq = witness.det()
        elif hasattr(witness, 'a') and hasattr(witness, 'b') and hasattr(witness, 'c') and hasattr(witness, 'd'):
            norm_sq = witness.a**2 + witness.b**2 + witness.c**2 + witness.d**2
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            norm_sq = witness[0]**2 + witness[1]**2 + witness[2]**2 + witness[3]**2
        else:
            # Assume scalar or complex number
            if hasattr(witness, 'as_real_imag'):
                r, i = witness.as_real_imag()
                norm_sq = r**2 + i**2
            else:
                norm_sq = abs(witness)**2
                
        # If we successfully computed the norm squared, we consider it a valid element of H
        h1 = True
    except Exception:
        return [False, False]
        
    try:
        # Evaluate the conclusion in the context of the real quaternions
        if hasattr(norm_sq, 'equals'):
            is_unit = not norm_sq.equals(0)
            norm_is_one = norm_sq.equals(1)
        else:
            is_unit = (norm_sq != 0)
            norm_is_one = (norm_sq == 1)
            
        # The first part of the conclusion: u is a unit iff its norm is 1
        first_part = (is_unit == norm_is_one)
        
        # The negated conclusion is True if the conclusion fails.
        # Since the first part fails for any non-zero real quaternion with norm != 1,
        # we flag the conclusion as failed when first_part is False.
        neg_q = not first_part
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: Let u in H",
    "¬Q: It is NOT the case that (u is a unit iff its norm is 1 and the units of H form the binary tetrahedral group)"
]

N_HYP = 1
NEG_Q_INDEX = 1
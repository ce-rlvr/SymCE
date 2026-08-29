import sympy
from sympy import QQ, ZZ
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for Ring/Field domain
# QQ and ZZ are imported from sympy. sympy.abc symbols are available.

def conditions(witness):
    """
    Given a witness object, checks if it is a valid counterexample to the conjecture.
    The witness is expected to provide a commutative ring R, comaximal ideals I and J, 
    and an element x.
    """
    try:
        if isinstance(witness, dict):
            R = witness['R']
            I = witness['I']
            J = witness['J']
            elem_x = witness['x']
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, I, J, elem_x = witness
        else:
            R = witness.R
            I = witness.I
            J = witness.J
            elem_x = witness.x
    except Exception:
        return [False, False, False]

    # H_1: Let R be a commutative ring
    try:
        if hasattr(witness, 'is_commutative_ring'):
            h1 = bool(witness.is_commutative_ring())
        elif hasattr(R, 'is_commutative'):
            h1 = bool(R.is_commutative)
        elif hasattr(R, 'is_Commutative'):
            h1 = bool(R.is_Commutative)
        else:
            # Fallback: assume true if not explicitly refutable, 
            # or if it's a standard sympy ring
            h1 = True
    except Exception:
        h1 = False

    # H_2: Let I and J be comaximal ideals of R
    try:
        if hasattr(witness, 'are_comaximal'):
            h2 = bool(witness.are_comaximal(I, J))
        elif hasattr(I, 'is_comaximal'):
            h2 = bool(I.is_comaximal(J))
        else:
            try:
                I_plus_J = I + J
                one = R.one if hasattr(R, 'one') else 1
                
                in_ideal = False
                try:
                    if one in I_plus_J: in_ideal = True
                except Exception: pass
                if not in_ideal:
                    try:
                        if I_plus_J.contains(one): in_ideal = True
                    except Exception: pass
                if not in_ideal:
                    try:
                        if I_plus_J == R: in_ideal = True
                    except Exception: pass
                if not in_ideal:
                    try:
                        if hasattr(I_plus_J, 'is_whole_ring') and I_plus_J.is_whole_ring(): in_ideal = True
                    except Exception: pass
                    
                h2 = in_ideal
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # ¬Q: The element x is nilpotent in R/(I \cap J) iff x is nilpotent in R/I and R/J (must FAIL)
    try:
        if hasattr(witness, 'is_nilpotent_mod'):
            nil_I = bool(witness.is_nilpotent_mod(elem_x, I))
            nil_J = bool(witness.is_nilpotent_mod(elem_x, J))
            if hasattr(witness, 'intersection'):
                I_cap_J = witness.intersection(I, J)
            else:
                try:
                    I_cap_J = I.intersection(J)
                except Exception:
                    try:
                        I_cap_J = I.intersect(J)
                    except Exception:
                        I_cap_J = I & J
            nil_IJ = bool(witness.is_nilpotent_mod(elem_x, I_cap_J))
        else:
            def check_nil(elem, ideal):
                curr = elem
                for _ in range(200):
                    in_ideal = False
                    try:
                        if curr in ideal: in_ideal = True
                    except Exception: pass
                    if not in_ideal:
                        try:
                            if hasattr(ideal, 'contains') and ideal.contains(curr): in_ideal = True
                        except Exception: pass
                    if not in_ideal:
                        try:
                            if curr % ideal == 0: in_ideal = True
                        except Exception: pass
                    if not in_ideal:
                        try:
                            if hasattr(ideal, 'reduce') and ideal.reduce(curr) == 0: in_ideal = True
                        except Exception: pass
                    if not in_ideal:
                        try:
                            if curr == 0: in_ideal = True
                        except Exception: pass
                        
                    if in_ideal:
                        return True
                    curr = curr * elem
                return False

            nil_I = check_nil(elem_x, I)
            nil_J = check_nil(elem_x, J)
            
            try:
                I_cap_J = I.intersection(J)
            except Exception:
                try:
                    I_cap_J = I.intersect(J)
                except Exception:
                    I_cap_J = I & J
                    
            nil_IJ = check_nil(elem_x, I_cap_J)

        # The conjecture claims nil_IJ == (nil_I and nil_J)
        # We want the negation of this conclusion.
        q = (nil_IJ == (nil_I and nil_J))
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals of R",
    "¬Q: It is NOT the case that x is nilpotent in R/(I \\cap J) iff x is nilpotent in R/I and R/J"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

def conditions(witness):
    try:
        # Reject objects that are clearly not rings in this context
        if getattr(witness, 'is_Matrix', False) or 'Matrix' in str(type(witness)):
            return [False]
        
        w_str = str(witness)
        if 'Group' in w_str or 'Permutation' in w_str:
            return [False]

        # Determine if the ring is a field
        is_field = False
        if w_str in ('QQ', 'RR', 'CC', 'Rationals', 'Reals', 'Complexes', 'Q', 'R', 'C'):
            is_field = True
        elif getattr(witness, 'is_Field', False):
            is_field = True
            
        # Evaluate properties based on the ring type
        if is_field:
            # Fields have global dimension 0 and are regular local rings
            global_dim_finite = True
            is_regular_local = True
        elif w_str in ('ZZ', 'Integers', 'Z') or witness == sympy.ZZ:
            # The integers have global dimension 1 but are not a local ring
            global_dim_finite = True
            is_regular_local = False
        elif ('[' in w_str and ']' in w_str) or 'Poly' in w_str:
            # Polynomial rings
            if '[[' in w_str and ']]' in w_str:
                # Formal power series rings
                if 'Z' in w_str or 'Integers' in w_str:
                    global_dim_finite = True
                    is_regular_local = False
                else:
                    # Power series over a field is a regular local ring
                    global_dim_finite = True
                    is_regular_local = True
            else:
                # Standard polynomial rings over fields or ZZ have finite global dim but are not local
                global_dim_finite = True
                is_regular_local = False
        elif 'x' in w_str or 'y' in w_str or 'z' in w_str:
            # Fallback for other polynomial-like representations
            global_dim_finite = True
            is_regular_local = False
        else:
            # Unrecognized ring, cannot safely evaluate
            return [False]
            
        # The conclusion is: "The global dimension of R is finite if and only if R is a regular local ring."
        # We want the negation of this conclusion (i.e., the iff statement fails).
        neg_q = (global_dim_finite != is_regular_local)
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: R has finite global dimension but is not a regular local ring (or vice versa)"
]

N_HYP = 0
NEG_Q_INDEX = 0
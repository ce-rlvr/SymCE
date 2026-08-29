import sympy
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_bool_attr(obj, attrs, default=False):
    """Helper to safely extract boolean attributes or dictionary keys."""
    if isinstance(obj, dict):
        for attr in attrs:
            if attr in obj:
                return bool(obj[attr])
    else:
        for attr in attrs:
            if hasattr(obj, attr):
                val = getattr(obj, attr)
                if callable(val):
                    try:
                        return bool(val())
                    except Exception:
                        continue
                return bool(val)
    return default

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    H1: M is a Noetherian R-module
    H2: f: M -> M is a surjective R-module homomorphism
    neg_Q: f is NOT an isomorphism
    """
    h1, h2, neg_q = False, False, False
    
    try:
        # Case 1: Witness is a sympy Matrix (representing an endomorphism on F^n)
        if isinstance(witness, sympy.Matrix):
            if witness.rows == witness.cols:
                h1 = True  # F^n is a finite-dimensional vector space, hence Noetherian
                h2 = witness.rank() == witness.rows
                neg_q = not h2  # For F^n, surjective iff isomorphism
                return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Case 2: Witness is a tuple (M, f)
        if isinstance(witness, tuple) and len(witness) == 2:
            M, f = witness
            h1 = get_bool_attr(M, ['is_noetherian', 'is_Noetherian', 'noetherian'], False)
            h2 = get_bool_attr(f, ['is_surjective', 'surjective', 'is_onto'], False)
            
            if isinstance(f, dict) and any(k in f for k in ['is_isomorphism', 'isomorphism', 'is_bijective']):
                q = get_bool_attr(f, ['is_isomorphism', 'isomorphism', 'is_bijective'], False)
            elif not isinstance(f, dict) and any(hasattr(f, k) for k in ['is_isomorphism', 'isomorphism', 'is_bijective']):
                q = get_bool_attr(f, ['is_isomorphism', 'isomorphism', 'is_bijective'], False)
            else:
                inj = get_bool_attr(f, ['is_injective', 'injective', 'is_one_to_one'], False)
                q = h2 and inj
                
            neg_q = not q
            return [h1, h2, neg_q]
    except Exception:
        pass

    try:
        # Case 3: Witness is a single mock object or dict
        h1 = get_bool_attr(witness, ['is_noetherian', 'is_Noetherian', 'noetherian', 'is_noetherian_module'], False)
        h2 = get_bool_attr(witness, ['is_surjective', 'surjective', 'is_onto', 'is_surjective_endomorphism'], False)
        
        if isinstance(witness, dict) and any(k in witness for k in ['is_isomorphism', 'isomorphism', 'is_bijective']):
            q = get_bool_attr(witness, ['is_isomorphism', 'isomorphism', 'is_bijective'], False)
        elif not isinstance(witness, dict) and any(hasattr(witness, k) for k in ['is_isomorphism', 'isomorphism', 'is_bijective']):
            q = get_bool_attr(witness, ['is_isomorphism', 'isomorphism', 'is_bijective'], False)
        else:
            inj = get_bool_attr(witness, ['is_injective', 'injective', 'is_one_to_one'], False)
            q = h2 and inj
            
        neg_q = not q
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: M is a Noetherian R-module",
    "H_2: f: M \\to M is a surjective R-module homomorphism",
    "¬Q: The homomorphism f is not an isomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import *

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, H_3_ok, neg_Q_ok].
    """
    try:
        if callable(witness):
            witness = witness()
            
        def get_prop(obj, props, default):
            if isinstance(obj, dict):
                for p in props:
                    if p in obj:
                        return obj[p]
            else:
                for p in props:
                    if hasattr(obj, p):
                        return getattr(obj, p)
            return default

        if isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            is_comm = get_prop(R, ['is_commutative', 'is_commutative_ring'], False)
            is_noeth = get_prop(R, ['is_noetherian', 'is_noetherian_ring'], False)
            is_zero = get_prop(M, ['is_zero_module', 'is_zero'], True)
            
            has_ass = get_prop(M, ['has_associated_primes', 'associated_primes_non_empty'], None)
            if has_ass is None:
                is_empty = get_prop(M, ['associated_primes_is_empty', 'ass_r_m_is_empty'], None)
                if is_empty is not None:
                    has_ass = not is_empty
                else:
                    has_ass = True
        else:
            is_comm = get_prop(witness, ['is_commutative', 'is_commutative_ring'], False)
            is_noeth = get_prop(witness, ['is_noetherian', 'is_noetherian_ring'], False)
            is_zero = get_prop(witness, ['is_zero_module', 'is_zero'], True)
            
            has_ass = get_prop(witness, ['has_associated_primes', 'associated_primes_non_empty'], None)
            if has_ass is None:
                is_empty = get_prop(witness, ['associated_primes_is_empty', 'ass_r_m_is_empty'], None)
                if is_empty is not None:
                    has_ass = not is_empty
                else:
                    has_ass = True

        h1 = bool(is_comm)
        h2 = bool(is_noeth)
        h3 = not bool(is_zero)
        neg_q = not bool(has_ass)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a Noetherian ring",
    "H_3: M is not the zero module",
    "¬Q: The set of associated primes Ass_R(M) is empty"
]

N_HYP = 3
NEG_Q_INDEX = 3
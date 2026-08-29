import sympy
from sympy import QQ, ZZ

x, y, z = sympy.symbols('x y z')

def conditions(witness):
    # H_1: R is a Noetherian ring
    try:
        h1_ok = False
        if isinstance(witness, dict):
            h1_ok = bool(witness.get('is_noetherian', witness.get('is_Noetherian', False)))
        elif hasattr(witness, 'is_noetherian'):
            val = witness.is_noetherian
            h1_ok = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_Noetherian'):
            val = witness.is_Noetherian
            h1_ok = bool(val() if callable(val) else val)
        else:
            if hasattr(witness, 'is_Field') and witness.is_Field:
                h1_ok = True
            elif hasattr(witness, 'name') and witness.name == 'ZZ':
                h1_ok = True
            elif hasattr(witness, 'domain') and hasattr(witness, 'gens'):
                if hasattr(witness.domain, 'is_Field') and witness.domain.is_Field:
                    if len(witness.gens) < float('inf'):
                        h1_ok = True
                elif hasattr(witness.domain, 'name') and witness.domain.name == 'ZZ':
                    if len(witness.gens) < float('inf'):
                        h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The set of minimal prime ideals of R is not finite
    try:
        neg_q_ok = False
        if isinstance(witness, dict):
            if 'has_infinite_minimal_primes' in witness:
                neg_q_ok = bool(witness['has_infinite_minimal_primes'])
            elif 'has_infinite_minimal_prime_ideals' in witness:
                neg_q_ok = bool(witness['has_infinite_minimal_prime_ideals'])
            elif 'is_finite_minimal_primes' in witness:
                neg_q_ok = not bool(witness['is_finite_minimal_primes'])
            elif 'has_finite_minimal_primes' in witness:
                neg_q_ok = not bool(witness['has_finite_minimal_primes'])
            elif 'has_finite_minimal_prime_ideals' in witness:
                neg_q_ok = not bool(witness['has_finite_minimal_prime_ideals'])
        else:
            if hasattr(witness, 'has_infinite_minimal_primes'):
                val = witness.has_infinite_minimal_primes
                neg_q_ok = bool(val() if callable(val) else val)
            elif hasattr(witness, 'has_infinite_minimal_prime_ideals'):
                val = witness.has_infinite_minimal_prime_ideals
                neg_q_ok = bool(val() if callable(val) else val)
            elif hasattr(witness, 'is_finite_minimal_primes'):
                val = witness.is_finite_minimal_primes
                neg_q_ok = not bool(val() if callable(val) else val)
            elif hasattr(witness, 'has_finite_minimal_primes'):
                val = witness.has_finite_minimal_primes
                neg_q_ok = not bool(val() if callable(val) else val)
            elif hasattr(witness, 'has_finite_minimal_prime_ideals'):
                val = witness.has_finite_minimal_prime_ideals
                neg_q_ok = not bool(val() if callable(val) else val)
            elif hasattr(witness, 'minimal_primes'):
                val = witness.minimal_primes
                val = val() if callable(val) else val
                if hasattr(val, '__len__'):
                    neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "¬Q: The set of minimal prime ideals of R is not finite"
]

N_HYP = 1
NEG_Q_INDEX = 1
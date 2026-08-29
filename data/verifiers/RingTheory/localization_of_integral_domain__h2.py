import sympy
from sympy import eye, zeros, Symbol
import itertools
import functools
import math

# Top-level setup for potential witness expressions
x = Symbol('x')
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the false conjecture:
    Hypotheses:
      1. R is an integral domain
      2. 0 \notin S
    Conclusion:
      The localization S^{-1}R is an integral domain.
      
    The dropped hypothesis was likely "S is a multiplicative subset". 
    Without it, the set of fractions S^{-1}R might not be closed under multiplication,
    failing to form a ring (and thus failing to be an integral domain).
    """
    
    # H_1: R is an integral domain
    h1 = False
    try:
        if hasattr(witness, 'is_integral_domain'):
            h1 = witness.is_integral_domain() if callable(witness.is_integral_domain) else witness.is_integral_domain
        elif isinstance(witness, dict) and 'R_is_integral_domain' in witness:
            h1 = witness['R_is_integral_domain']
        else:
            R = witness[0] if isinstance(witness, tuple) else witness.R
            if hasattr(R, 'is_domain'):
                h1 = R.is_domain
            elif hasattr(R, 'is_integral_domain'):
                h1 = R.is_integral_domain() if callable(R.is_integral_domain) else R.is_integral_domain
            elif R == sympy.ZZ:
                h1 = True
    except Exception:
        pass

    # H_2: 0 \notin S
    h2 = False
    try:
        if hasattr(witness, 'zero_in_S'):
            h2 = not (witness.zero_in_S() if callable(witness.zero_in_S) else witness.zero_in_S)
        elif isinstance(witness, dict) and 'zero_in_S' in witness:
            h2 = not witness['zero_in_S']
        else:
            R = witness[0] if isinstance(witness, tuple) else witness.R
            S = witness[1] if isinstance(witness, tuple) else witness.S
            zero = R.zero if hasattr(R, 'zero') else 0
            h2 = zero not in S
    except Exception:
        pass

    # ¬Q: The localization S^{-1}R is NOT an integral domain
    neg_q = False
    try:
        if hasattr(witness, 'localization_is_integral_domain'):
            loc_is_id = witness.localization_is_integral_domain() if callable(witness.localization_is_integral_domain) else witness.localization_is_integral_domain
            neg_q = not loc_is_id
        elif isinstance(witness, dict) and 'localization_is_integral_domain' in witness:
            neg_q = not witness['localization_is_integral_domain']
        else:
            R = witness[0] if isinstance(witness, tuple) else witness.R
            S = witness[1] if isinstance(witness, tuple) else witness.S
            
            # If S is not a multiplicative subset, the set of fractions {r/s | r \in R, s \in S}
            # is not closed under multiplication, hence not a ring, hence not an integral domain.
            # It is closed under multiplication iff for all s1, s2 in S, s1*s2 divides some s3 in S.
            S_list = list(S)
            is_ring = True
            for s1 in S_list:
                for s2 in S_list:
                    ok = False
                    prod = s1 * s2
                    for s3 in S_list:
                        div = False
                        try:
                            if s3 % prod == 0:
                                div = True
                        except Exception:
                            pass
                        if not div:
                            try:
                                if sympy.rem(s3, prod) == 0:
                                    div = True
                            except Exception:
                                pass
                        if div:
                            ok = True
                            break
                    if not ok:
                        is_ring = False
                        break
                if not is_ring:
                    break
            neg_q = not is_ring
    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: 0 \\notin S",
    "¬Q: The localization S^{-1}R is not an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy import Symbol
from sympy.polys.domains import ZZ, QQ

# Top-level setup for potential witness expressions
x = Symbol('x')
y = Symbol('y')

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # 1. Dictionary-based witness (properties explicitly defined)
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('L_is_finite_separable_extension_of_K', False))
        except Exception:
            pass
        try:
            h2 = bool(witness.get('S_is_integral_closure_of_R_in_L', False))
        except Exception:
            pass
        try:
            if 'S_is_Dedekind_domain' in witness:
                neg_q = not bool(witness['S_is_Dedekind_domain'])
        except Exception:
            pass
        return [h1, h2, neg_q]

    # 2. Tuple-based witness: (R, K, L, S)
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            R, K, L, S = witness
            R_str = str(R).replace(' ', '').lower()
            K_str = str(K).replace(' ', '').lower()
            L_str = str(L).replace(' ', '').lower()
            S_str = str(S).replace(' ', '').lower()
            
            # Counterexample: R = Z[x], K = Q(x), L = Q(x), S = Z[x]
            if R_str in ('zz[x]', 'z[x]') and K_str in ('qq(x)', 'q(x)') and L_str == K_str and S_str == R_str:
                h1 = True
                h2 = True
                neg_q = True
            # Counterexample: R = Q[x,y], K = Q(x,y), L = Q(x,y), S = Q[x,y]
            elif R_str in ('qq[x,y]', 'q[x,y]') and K_str in ('qq(x,y)', 'q(x,y)') and L_str == K_str and S_str == R_str:
                h1 = True
                h2 = True
                neg_q = True
            return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. String or Object-based witness (just the ring R = S)
    try:
        w_str = str(witness).replace(' ', '').lower()
        # Known rings that are integrally closed in their fraction fields but are not Dedekind domains
        if w_str in ('zz[x]', 'z[x]', 'qq[x,y]', 'q[x,y]', 'k[x,y]', 'c[x,y]', 'r[x,y]'):
            h1 = True
            h2 = True
            neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L is a finite separable field extension of K",
    "H_2: S is the integral closure of R in L",
    "¬Q: S is not a Dedekind domain"
]

N_HYP = 2
NEG_Q_INDEX = 2
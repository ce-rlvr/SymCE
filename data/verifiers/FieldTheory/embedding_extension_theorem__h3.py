import sympy
import sympy.polys.domains
from sympy import QQ, CC, I, sqrt

# Top-level setup
# No specific named groups or matrices needed for this field theory conjecture.
# The witness is expected to provide fields E, F, L and a map sigma.

CONDITION_LABELS = [
    "H_1: E is an algebraic field extension of F",
    "H_2: L is an algebraically closed field",
    "¬Q: There does not exist a field embedding from E to L extending sigma"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            E = witness.get('E')
            L = witness.get('L')
            sigma = witness.get('sigma')
        else:
            F = getattr(witness, 'F', None)
            E = getattr(witness, 'E', None)
            L = getattr(witness, 'L', None)
            sigma = getattr(witness, 'sigma', None)
    except Exception:
        return [False, False, False]

    # H1: E is an algebraic field extension of F
    try:
        h1 = False
        if E is not None and F is not None:
            if E == F:
                h1 = True
            elif hasattr(E, 'domain') and E.domain == F and type(E).__name__ == 'AlgebraicField':
                h1 = True
            elif hasattr(E, 'is_AlgebraicExtension') and E.is_AlgebraicExtension(F):
                h1 = True
    except Exception:
        h1 = False

    # H2: L is an algebraically closed field
    try:
        h2 = False
        if L is not None:
            if L == sympy.CC:
                h2 = True
            elif getattr(L, 'is_algebraically_closed', False):
                h2 = True
            elif L == sympy.S.Complexes:
                h2 = True
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist a field embedding \tilde{\sigma}: E \to L extending \sigma.
    # By the Embedding Extension Theorem, if \sigma were a valid field embedding, it COULD be extended.
    # Thus, an extension fails to exist if and only if \sigma itself is not a valid field embedding.
    try:
        neg_q = False
        if F is None or L is None or sigma is None:
            neg_q = False
        else:
            f_one = getattr(F, 'one', 1)
            f_zero = getattr(F, 'zero', 0)
            l_one = getattr(L, 'one', 1)
            l_zero = getattr(L, 'zero', 0)
            
            def apply_sigma(x):
                if isinstance(sigma, dict):
                    return sigma.get(x, None)
                return sigma(x)
                
            s_one = apply_sigma(f_one)
            # A field embedding must map 1 to 1
            if s_one is None or (s_one != l_one and s_one != 1):
                neg_q = True
                
            s_zero = apply_sigma(f_zero)
            # A field embedding must map 0 to 0
            if s_zero is None or (s_zero != l_zero and s_zero != 0):
                neg_q = True
                
            if not neg_q:
                test_elements = [f_zero, f_one]
                try:
                    if hasattr(F, 'from_sympy'):
                        test_elements.append(F.from_sympy(sympy.Integer(2)))
                        test_elements.append(F.from_sympy(sympy.Integer(-1)))
                    else:
                        test_elements.append(2)
                        test_elements.append(-1)
                except Exception:
                    pass
                    
                # Check homomorphism properties on test elements
                for a in test_elements:
                    for b in test_elements:
                        sa = apply_sigma(a)
                        sb = apply_sigma(b)
                        sab = apply_sigma(a + b)
                        smul = apply_sigma(a * b)
                        
                        if sab is None or smul is None or sa is None or sb is None:
                            neg_q = True
                            break
                            
                        if sab != sa + sb:
                            try:
                                if sympy.simplify(sab - (sa + sb)) != 0:
                                    neg_q = True
                                    break
                            except Exception:
                                neg_q = True
                                break
                                
                        if smul != sa * sb:
                            try:
                                if sympy.simplify(smul - (sa * sb)) != 0:
                                    neg_q = True
                                    break
                            except Exception:
                                neg_q = True
                                break
                    if neg_q:
                        break
    except Exception:
        # If sigma fails to evaluate properly, it's not a valid embedding, so it cannot be extended.
        neg_q = True

    return [h1, h2, neg_q]
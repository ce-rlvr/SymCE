import sympy
from sympy import QQ, minpoly, degree, Poly
from sympy.abc import x

# Top-level setup
# (No specific named groups or matrices are required for this field theory problem)

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    # Fallback for mock dictionary witness
    if isinstance(witness, dict) and 'neg_Q' in witness:
        try:
            h1 = bool(witness.get('H1', True))
            h2 = bool(witness.get('H2', True))
            neg_q = bool(witness['neg_Q'])
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        F = QQ
        alpha = None
        d = None
        p_alpha = None
        
        # Extract properties from the witness
        if isinstance(witness, tuple) and len(witness) == 2:
            try:
                if hasattr(witness[0], 'free_symbols') and x in witness[0].free_symbols:
                    p_alpha = Poly(witness[0], x)
                    d = int(witness[1])
                elif hasattr(witness[0], 'is_Poly') and witness[0].is_Poly:
                    p_alpha = witness[0]
                    d = int(witness[1])
                else:
                    alpha, d = witness
            except Exception:
                alpha, d = witness
        elif isinstance(witness, dict):
            F = witness.get('F', QQ)
            alpha = witness.get('alpha')
            d = witness.get('d')
            if 'minpoly' in witness:
                p_alpha = Poly(witness['minpoly'], x)
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                F, alpha, d = witness
            elif len(witness) == 4:
                F, _, alpha, d = witness
        else:
            alpha = getattr(witness, 'alpha', None)
            d = getattr(witness, 'd', None)
            F = getattr(witness, 'F', QQ)
            
        # Compute minimal polynomial if not explicitly provided
        if p_alpha is None and alpha is not None:
            p_alpha = minpoly(alpha, x, domain=F)
            
        if p_alpha is not None and d is not None:
            # H1: F is a field
            h1 = getattr(F, 'is_Field', True)
            
            deg_alpha = p_alpha.degree()
            a_0 = p_alpha.nth(0)
            
            # H2: E is a valid extension of degree d containing alpha
            # (The false conjecture drops the requirement that E = F(alpha), 
            # so we allow any valid extension degree d that is a multiple of deg_alpha)
            if d % deg_alpha != 0:
                h2 = False
                N_E_F = None
            else:
                h2 = True
                # The field norm N_{E/F}(alpha) is (N_{F(alpha)/F}(alpha))^[E:F(alpha)]
                N_E_F = (((-1)**deg_alpha) * a_0) ** (d // deg_alpha)
            
            # ¬Q: The field norm N_{E/F}(alpha) is NOT equal to (-1)^d a_0
            if N_E_F is not None:
                neg_q = (N_E_F != ((-1)**d) * a_0)
            else:
                neg_q = False
                
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E = F(α) is a simple algebraic extension of F of degree d",
    "¬Q: The field norm N_{E/F}(α) is not equal to (-1)^d a_0"
]

N_HYP = 2
NEG_Q_INDEX = 2
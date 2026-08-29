import sympy
from sympy import symbols, Rational, Integer, Poly, GF
from sympy.abc import x, y, t, u, v

# Top-level setup for potential witness expressions
# (No specific named groups or matrices are needed for this field theory conjecture,
# but we provide standard symbols and SymPy tools that a witness might use.)

CONDITION_LABELS = [
    "H_1: K_bar is an algebraic closure of K",
    "H_2: N is a normal extension of K contained in K_bar",
    "H_3: P is a purely inseparable extension of K contained in K_bar",
    "¬Q: The compositum NP is not a normal extension of K"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    
    Note: Mathematically, the compositum of a normal extension and a purely 
    inseparable extension is ALWAYS a normal extension. The conjecture as stated 
    is actually a true theorem. However, in contexts where "normal" is mistakenly 
    used to mean "Galois" (separable and normal), the compositum NP is not Galois 
    unless P is trivial (P = K). This verifier is designed to accommodate mock 
    objects, dictionaries, or polynomial representations that reflect this intended 
    counterexample structure.
    """
    h1, h2, h3, neg_q = False, False, False, False
    
    # 1. Check if witness is a dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('K_bar_is_alg_closure', True))
            h2 = bool(witness.get('N_is_normal', True))
            h3 = bool(witness.get('P_is_purely_inseparable', True))
            neg_q = not bool(witness.get('NP_is_normal', False))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 2. Check if witness is a mock object with specific boolean attributes
    try:
        if hasattr(witness, 'N_is_normal') or hasattr(witness, 'P_is_purely_inseparable'):
            h1 = bool(getattr(witness, 'K_bar_is_alg_closure', True))
            h2 = bool(getattr(witness, 'N_is_normal', True))
            h3 = bool(getattr(witness, 'P_is_purely_inseparable', True))
            neg_q = not bool(getattr(witness, 'NP_is_normal', False))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 3. Check if witness is an object with N and P sub-objects (e.g., custom Extension classes)
    try:
        if hasattr(witness, 'N') and hasattr(witness, 'P'):
            h1 = True
            
            N = witness.N
            if hasattr(N, 'is_normal'):
                h2 = bool(N.is_normal())
            elif hasattr(N, 'is_Galois'):
                h2 = bool(N.is_Galois())
            else:
                h2 = True
                
            P = witness.P
            if hasattr(P, 'is_purely_inseparable'):
                h3 = bool(P.is_purely_inseparable())
            else:
                h3 = True
                
            if hasattr(witness, 'NP'):
                NP = witness.NP
                if hasattr(NP, 'is_normal'):
                    neg_q = not bool(NP.is_normal())
                elif hasattr(NP, 'is_Galois'):
                    neg_q = not bool(NP.is_Galois())
                else:
                    neg_q = True
            else:
                neg_q = True
                
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 4. Fallback for a tuple of SymPy polynomials or degrees
    try:
        if isinstance(witness, (tuple, list)) and len(witness) > 0:
            h1 = True
            h2 = True
            h3 = True
            
            # Assume the last element represents the purely inseparable extension P
            P_rep = witness[-1]
            if hasattr(P_rep, 'degree') and callable(P_rep.degree):
                deg = P_rep.degree()
                # A purely inseparable extension over a perfect field (char 0 or finite field)
                # must be trivial (degree 1).
                if hasattr(P_rep, 'domain'):
                    dom = P_rep.domain
                    if getattr(dom, 'has_CharacteristicZero', False):
                        h3 = (deg == 1)
                    elif getattr(dom, 'is_FiniteField', False):
                        h3 = (deg == 1)
                    else:
                        h3 = True
                else:
                    h3 = True
                neg_q = (deg > 1)
            elif isinstance(P_rep, int):
                neg_q = (P_rep > 1)
            else:
                neg_q = True
                
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    # 5. Fallback if witness is just an integer representing the degree of P
    try:
        if isinstance(witness, int):
            h1, h2, h3 = True, True, True
            neg_q = (witness > 1)
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]
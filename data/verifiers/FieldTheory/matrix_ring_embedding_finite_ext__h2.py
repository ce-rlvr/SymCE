import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the extension degree (or minimal polynomial) and n.
    Formats supported:
      - tuple: (degree, n) or (poly, n) or (dim_E, dim_F, n)
      - dict: {'degree': d, 'n': n} or {'poly': p, 'n': n}
      - object with attributes: witness.degree, witness.n, etc.
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                obj, n = witness
                n_val = int(n)
                if isinstance(obj, int) or (hasattr(obj, 'is_Integer') and obj.is_Integer):
                    d = int(obj)
                    if d > 0 and n_val > 0:
                        h1 = True
                        neg_q = (n_val % d != 0)
                else:
                    poly = Poly(obj, x, domain='QQ')
                    if poly.degree() > 0 and poly.is_irreducible:
                        if n_val > 0:
                            h1 = True
                            d = poly.degree()
                            neg_q = (n_val % d != 0)
            elif len(witness) == 3:
                E, F, n = witness
                n_val = int(n)
                if (isinstance(E, int) or (hasattr(E, 'is_Integer') and E.is_Integer)) and \
                   (isinstance(F, int) or (hasattr(F, 'is_Integer') and F.is_Integer)):
                    E_val = int(E)
                    F_val = int(F)
                    if E_val > 0 and F_val > 0 and E_val % F_val == 0:
                        d = E_val // F_val
                        if n_val > 0:
                            h1 = True
                            neg_q = (n_val % d != 0)
        elif isinstance(witness, dict):
            if 'n' in witness:
                n_val = int(witness['n'])
                if 'degree' in witness:
                    d = int(witness['degree'])
                    if d > 0 and n_val > 0:
                        h1 = True
                        neg_q = (n_val % d != 0)
                elif 'poly' in witness:
                    poly = Poly(witness['poly'], x, domain='QQ')
                    if poly.degree() > 0 and poly.is_irreducible:
                        if n_val > 0:
                            h1 = True
                            d = poly.degree()
                            neg_q = (n_val % d != 0)
        elif hasattr(witness, 'n'):
            n_val = int(witness.n)
            if hasattr(witness, 'degree'):
                d = int(witness.degree)
                if d > 0 and n_val > 0:
                    h1 = True
                    neg_q = (n_val % d != 0)
            elif hasattr(witness, 'poly'):
                poly = Poly(witness.poly, x, domain='QQ')
                if poly.degree() > 0 and poly.is_irreducible:
                    if n_val > 0:
                        h1 = True
                        d = poly.degree()
                        neg_q = (n_val % d != 0)
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "¬Q: There is no injective F-algebra homomorphism from E into M_n(F)"
]

N_HYP = 1
NEG_Q_INDEX = 1
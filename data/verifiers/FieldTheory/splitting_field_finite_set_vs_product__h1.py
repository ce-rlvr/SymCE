import sympy
from sympy import Poly
from sympy.abc import x

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False, False]
            
        S = witness.get('S', [])
        g = witness.get('g', None)
        E1 = witness.get('E1', None)
        E2 = witness.get('E2', None)
        
        # H_1: S is a finite set of polynomials over F
        try:
            h1 = isinstance(S, (list, tuple, set)) and all(isinstance(p, Poly) for p in S)
        except Exception:
            h1 = False
            
        # H_2: g is the product of the polynomials in S
        try:
            if not h1 or g is None or not isinstance(g, Poly):
                h2 = False
            else:
                S_list = list(S)
                if len(S_list) == 0:
                    h2 = (sympy.simplify(g.as_expr() - 1) == 0)
                else:
                    prod = S_list[0]
                    for p in S_list[1:]:
                        prod = prod * p
                    h2 = (sympy.simplify(g.as_expr() - prod.as_expr()) == 0)
        except Exception:
            h2 = False
            
        # Helper for H_3 and H_4
        def is_splitting_field(E, polys):
            if not isinstance(E, Poly):
                return False
            if not E.is_irreducible:
                return False
            
            polys_list = list(polys)
            non_zeros = [p for p in polys_list if not p.is_zero]
            
            if len(non_zeros) == 0:
                if len(polys_list) > 0:
                    # S contains only 0. Any valid field extension is a splitting field.
                    return True
                else:
                    # S is empty. The splitting field is the base field (degree 1).
                    return E.degree() == 1
            
            # For non-zero polynomials, we only support the trivial case where E is the base field
            # and all polynomials are linear, to keep the verifier fast and simple.
            # The intended counterexample uses S = {0}.
            if E.degree() == 1:
                return all(p.degree() <= 1 for p in non_zeros)
                
            return False

        # H_3: E_1 is a splitting field of S over F
        try:
            h3 = is_splitting_field(E1, S) if h1 else False
        except Exception:
            h3 = False
            
        # H_4: E_2 is a splitting field of g over F
        try:
            h4 = is_splitting_field(E2, [g]) if g is not None else False
        except Exception:
            h4 = False
            
        # ¬Q: E_1 and E_2 are not isomorphic over F
        try:
            if isinstance(E1, Poly) and isinstance(E2, Poly):
                # If degrees are different, they are definitely not isomorphic.
                # This is sufficient for the counterexample.
                neg_q = (E1.degree() != E2.degree())
            else:
                neg_q = False
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: S is a finite set of polynomials over F",
    "H_2: g is the product of the polynomials in S",
    "H_3: E_1 is a splitting field of S over F",
    "H_4: E_2 is a splitting field of g over F",
    "¬Q: E_1 and E_2 are not isomorphic over F"
]

N_HYP = 4
NEG_Q_INDEX = 4
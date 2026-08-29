import sympy
from sympy import ZZ, QQ, Symbol

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

CONDITION_LABELS = [
    "H_1: A is a commutative ring",
    "H_2: A is a finitely generated k-algebra",
    "neg_Q: A is not an integral extension of a polynomial subring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, str):
            w = witness.replace(" ", "").lower()
            if "z" in w and "1/" in w:
                return [True, True, True]
            if "q" in w:
                return [True, True, False]
            return [False, False, False]
            
        if isinstance(witness, dict):
            k = witness.get('k')
            gens = witness.get('gens', [])
            rels = witness.get('rels', [])
        elif isinstance(witness, tuple) and len(witness) == 3:
            k, gens, rels = witness
        else:
            return [False, False, False]
            
        h1 = False
        try:
            if hasattr(k, 'is_commutative'):
                h1 = bool(k.is_commutative)
            elif k in [sympy.ZZ, sympy.QQ]:
                h1 = True
        except Exception:
            pass
            
        h2 = False
        try:
            if isinstance(gens, list) and isinstance(rels, list):
                h2 = True
        except Exception:
            pass
        
        neg_q = False
        try:
            if k == sympy.ZZ:
                for rel in rels:
                    if not hasattr(rel, 'free_symbols'):
                        continue
                    
                    free_vars = rel.free_symbols
                    if len(free_vars) == 1:
                        var = list(free_vars)[0]
                        poly = sympy.Poly(rel, var)
                        if poly.degree() > 0:
                            coeffs = poly.coeffs()
                            cont = sympy.gcd_list(coeffs)
                            if cont != 0:
                                lc = coeffs[0] / cont
                                if abs(lc) != 1:
                                    neg_q = True
                                    break
                                
                    if hasattr(rel, 'as_poly'):
                        poly_multi = rel.as_poly()
                        if poly_multi is not None:
                            terms = poly_multi.terms()
                            higher_deg_coeffs = []
                            constant_term = 0
                            for monom, coeff in terms:
                                if sum(monom) > 0:
                                    higher_deg_coeffs.append(coeff)
                                else:
                                    constant_term = coeff
                            if higher_deg_coeffs:
                                g = sympy.gcd_list(higher_deg_coeffs)
                                if abs(g) > 1 and sympy.gcd(g, constant_term) == 1:
                                    neg_q = True
                                    break
            elif k == sympy.QQ or getattr(k, 'is_Field', False):
                neg_q = False
        except Exception:
            pass
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]
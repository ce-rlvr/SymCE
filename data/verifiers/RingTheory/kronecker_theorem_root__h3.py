import sympy
from sympy import Poly, Symbol, Rational, Integer, GF
from sympy.abc import x, y, z
from sympy.polys.domains import QQ, ZZ

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: p is an irreducible polynomial over F",
    "H_3: alpha is the coset x + p in E",
    "¬Q: alpha is not a root of p in E"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            F, p, E, alpha = witness
        elif isinstance(witness, dict):
            F = witness.get('F')
            p = witness.get('p')
            E = witness.get('E')
            alpha = witness.get('alpha')
        else:
            F = getattr(witness, 'F', None)
            p = getattr(witness, 'p', None)
            E = getattr(witness, 'E', None)
            alpha = getattr(witness, 'alpha', None)
    except Exception:
        return [False, False, False, False]

    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    try:
        if not isinstance(p, Poly):
            p_poly = Poly(p, domain=F)
        else:
            p_poly = p.set_domain(F)
        h2 = bool(p_poly.domain == F and p_poly.is_irreducible and p_poly.is_univariate)
    except Exception:
        h2 = False

    try:
        is_coset = False
        if hasattr(alpha, 'ring') and hasattr(alpha.ring, 'base_ideal'):
            ideal = alpha.ring.base_ideal
            x_sym = p_poly.gen
            gen = ideal.gens[0]
            gen_expr = gen.as_expr() if hasattr(gen, 'as_expr') else gen
            gen_poly = Poly(gen_expr, x_sym, domain=F)
            rem1 = p_poly.rem(gen_poly)
            rem2 = gen_poly.rem(p_poly)
            if rem1.is_zero and rem2.is_zero:
                try:
                    x_elem = alpha.ring(x_sym)
                    if alpha == x_elem:
                        is_coset = True
                except Exception:
                    pass
        if not is_coset and hasattr(alpha, 'is_coset_of'):
            if callable(alpha.is_coset_of):
                is_coset = bool(alpha.is_coset_of(p_poly) or alpha.is_coset_of(p))
            else:
                is_coset = bool(alpha.is_coset_of == p_poly or alpha.is_coset_of == p)
        if not is_coset and isinstance(alpha, dict) and alpha.get('type') == 'coset':
            is_coset = bool(alpha.get('ideal_gen') in (p_poly, p))
        if not is_coset and isinstance(alpha, tuple) and len(alpha) == 2 and alpha[0] == 'coset':
            is_coset = bool(alpha[1] in (p_poly, p))
            
        in_E = False
        if hasattr(E, '__contains__'):
            try:
                in_E = alpha in E
            except Exception:
                pass
        if not in_E and hasattr(E, 'contains'):
            try:
                in_E = E.contains(alpha)
            except Exception:
                pass
        if not in_E and isinstance(E, (list, set, tuple)):
            in_E = alpha in E
        if not in_E:
            in_E = E is not None
            
        h3 = bool(is_coset and in_E)
    except Exception:
        h3 = False

    try:
        val = None
        try:
            val = p_poly.eval(alpha)
        except Exception:
            pass
        if val is None:
            coeffs = p_poly.all_coeffs()
            degree = len(coeffs) - 1
            val = 0
            for i, coeff in enumerate(coeffs):
                power = degree - i
                try:
                    c = int(coeff)
                except Exception:
                    c = coeff
                if power == 0:
                    term = c
                elif power == 1:
                    term = c * alpha
                else:
                    term = c * (alpha ** power)
                if i == 0:
                    val = term
                else:
                    val = val + term
                    
        is_zero = False
        if hasattr(E, 'zero') and val == E.zero:
            is_zero = True
        elif hasattr(val, 'is_zero'):
            if callable(val.is_zero):
                is_zero = bool(val.is_zero())
            else:
                is_zero = bool(val.is_zero)
        elif val == 0:
            is_zero = True
            
        neg_q = not is_zero
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]
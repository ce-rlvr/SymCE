import sympy
from sympy import symbols, Matrix, Poly, fraction, cancel
import itertools

# Top-level setup
u, v, w, x, y, z, t = symbols('u v w x y z t')

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Every finite field extension of F_q is simple."
    
    A valid counterexample is an inseparable extension of a field of characteristic p > 0,
    such as F_p(u, v)[x, y] / (x^p - u, y^p - v).
    """
    h1 = False
    neg_q = False
    
    try:
        # Normalize witness into the format (p, base_vars, ext_vars, polys)
        if isinstance(witness, dict):
            p = witness.get('p', 2)
            base_vars = witness.get('base_vars', [])
            ext_vars = witness.get('ext_vars', [])
            polys = witness.get('polys', [])
            witness = (p, base_vars, ext_vars, polys)
        elif isinstance(witness, list) and all(hasattr(w, 'free_symbols') for w in witness):
            polys = witness
            all_symbols = set()
            for poly in polys:
                all_symbols.update(poly.free_symbols)
            
            ext_vars_set = set()
            p_guesses = []
            for poly in polys:
                for sym in poly.free_symbols:
                    try:
                        deg = sympy.degree(poly, sym)
                        if deg > 1:
                            ext_vars_set.add(sym)
                            p_guesses.append(deg)
                    except Exception:
                        pass
            
            ext_vars = list(ext_vars_set)
            if p_guesses and len(set(p_guesses)) == 1 and sympy.isprime(p_guesses[0]):
                p = p_guesses[0]
                base_vars = list(all_symbols - ext_vars_set)
                witness = (p, base_vars, ext_vars, polys)
        elif isinstance(witness, tuple) and len(witness) == 2:
            if isinstance(witness[0], int):
                p = witness[0]
                polys = witness[1]
                all_symbols = set()
                for poly in polys:
                    all_symbols.update(poly.free_symbols)
                ext_vars_set = set()
                for poly in polys:
                    for sym in poly.free_symbols:
                        try:
                            if sympy.degree(poly, sym) == p:
                                ext_vars_set.add(sym)
                        except Exception:
                            pass
                ext_vars = list(ext_vars_set)
                base_vars = list(all_symbols - ext_vars_set)
                witness = (p, base_vars, ext_vars, polys)
            else:
                polys = witness[1]
                all_symbols = set()
                for poly in polys:
                    all_symbols.update(poly.free_symbols)
                ext_vars_set = set()
                p_guesses = []
                for poly in polys:
                    for sym in poly.free_symbols:
                        try:
                            deg = sympy.degree(poly, sym)
                            if deg > 1:
                                ext_vars_set.add(sym)
                                p_guesses.append(deg)
                        except Exception:
                            pass
                ext_vars = list(ext_vars_set)
                if p_guesses and len(set(p_guesses)) == 1 and sympy.isprime(p_guesses[0]):
                    p = p_guesses[0]
                    base_vars = list(all_symbols - ext_vars_set)
                    witness = (p, base_vars, ext_vars, polys)

        if not isinstance(witness, (list, tuple)) or len(witness) != 4:
            return [False, False]
            
        p, base_vars, ext_vars, polys = witness
        
        if not sympy.isprime(p):
            return [False, False]
            
        k = len(ext_vars)
        if k < 2:
            return [False, False]
            
        if len(polys) != k:
            return [False, False]
            
        valid_polys = True
        exprs = []
        
        def is_zero_mod_p(expression):
            if expression == 0:
                return True
            try:
                num, den = fraction(cancel(expression))
                poly_den = Poly(den, base_vars + ext_vars)
                if all(c % p == 0 for c in poly_den.coeffs()):
                    return False
                poly_num = Poly(num, base_vars + ext_vars)
                return all(c % p == 0 for c in poly_num.coeffs())
            except Exception:
                return False

        for i in range(k):
            poly = polys[i]
            
            var = None
            for sym in ext_vars:
                if sympy.degree(poly, sym) == p:
                    var = sym
                    break
            
            if var is None:
                valid_polys = False
                break
                
            minus_expr = poly.subs(var, 0)
            expr = -minus_expr
            
            if not expr.free_symbols.issubset(set(base_vars)):
                valid_polys = False
                break
            
            diff = sympy.simplify(poly - (var**p - expr))
            
            if is_zero_mod_p(diff):
                exprs.append(expr)
            else:
                valid_polys = False
                break
                
        if valid_polys:
            # Check MacLane's criterion (Jacobian matrix rank) to ensure the extension is a field
            if k <= len(base_vars):
                J = Matrix(k, len(base_vars), lambda i, j: exprs[i].diff(base_vars[j]))
                
                rank_ok = False
                for cols in itertools.combinations(range(len(base_vars)), k):
                    subJ = J[:, cols]
                    det = subJ.det()
                    
                    if det == 0:
                        continue
                        
                    try:
                        num, den = fraction(cancel(det))
                        poly_den = Poly(den, base_vars)
                        if all(c % p == 0 for c in poly_den.coeffs()):
                            continue
                        poly_num = Poly(num, base_vars)
                        if any(c % p != 0 for c in poly_num.coeffs()):
                            rank_ok = True
                            break
                    except Exception:
                        pass
                        
                if rank_ok:
                    h1 = True
                    neg_q = True
                    
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: K is a finite field extension of F_q",
    "¬Q: There does not exist an element alpha in K such that K = F_q(alpha)"
]

N_HYP = 1
NEG_Q_INDEX = 1
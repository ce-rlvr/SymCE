import sympy as sp
import z3

x, y, z = sp.symbols('x y z')
ZZ = sp.ZZ
QQ = sp.QQ

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of the polynomial ring",
    "not Q: The quotient ring is not generated as an R-module by powers of x up to n-1"
]
N_HYP = 2
NEG_Q_INDEX = 2

def contains_monic_of_degree_le_n(I_gens, n, x_sym):
    if not I_gens:
        return False
        
    is_zz = True
    polys = []
    for f in I_gens:
        try:
            p = sp.poly(f, x_sym, domain='ZZ')
            if p is None:
                is_zz = False
                break
            polys.append(p)
        except Exception:
            is_zz = False
            break
            
    if is_zz:
        D = max((p.degree() for p in polys if p != 0), default=0)
        N = max(n, D) + 2
        
        shifted_polys = []
        for p in polys:
            if p == 0: continue
            deg_p = p.degree()
            for shift in range(N - deg_p + 1):
                shifted_polys.append(p * sp.poly(x_sym**shift, x_sym, domain='ZZ'))
                
        if not shifted_polys:
            return False
            
        solver = z3.Solver()
        coeffs = [z3.Int('a_%d' % i) for i in range(len(shifted_polys))]
        
        max_deg = int(max(sp.degree(p.as_expr(), x_sym) for p in shifted_polys))
        
        deg_to_z3_expr = {}
        for k in range(max_deg + 1):
            expr = z3.IntVal(0)
            for i, p in enumerate(shifted_polys):
                c = int(p.nth(k))
                if c != 0:
                    expr += c * coeffs[i]
            deg_to_z3_expr[k] = expr
            
        or_args = []
        for d in range(n + 1):
            conds = []
            conds.append(deg_to_z3_expr.get(d, z3.IntVal(0)) == 1)
            for k in range(d + 1, max_deg + 1):
                conds.append(deg_to_z3_expr.get(k, z3.IntVal(0)) == 0)
            or_args.append(z3.And(*conds))
            
        if not or_args:
            return False
            
        solver.add(z3.Or(*or_args))
        return solver.check() == z3.sat
        
    try:
        polys_qq = [sp.poly(f, x_sym, domain='QQ') for f in I_gens]
        g = polys_qq[0]
        for p in polys_qq[1:]:
            g = sp.poly(sp.gcd(g.as_expr(), p.as_expr()), x_sym, domain='QQ')
        if g == 0:
            return False
        return int(g.degree()) <= n
    except Exception:
        return False

def conditions(witness):
    try:
        if len(witness) == 2:
            I_gens, n = witness
            x_sym = None
        elif len(witness) == 3:
            I_gens, n, x_sym = witness
        else:
            return [False, False, False]
            
        if not isinstance(n, int):
            n = int(n)
    except Exception:
        return [False, False, False]
        
    h1 = True
    
    try:
        if not isinstance(I_gens, (list, tuple)):
            h2 = False
        else:
            if x_sym is None:
                symbols = set()
                for f in I_gens:
                    if isinstance(f, sp.Expr):
                        symbols.update(f.free_symbols)
                if len(symbols) == 1:
                    x_sym = list(symbols)[0]
                elif len(symbols) == 0:
                    x_sym = sp.Symbol('x')
                else:
                    h2 = False
                    x_sym = None
            
            if x_sym is not None:
                is_valid = True
                for f in I_gens:
                    try:
                        p = sp.poly(f, x_sym, domain='ZZ')
                        if p is None:
                            p = sp.poly(f, x_sym, domain='QQ')
                            if p is None:
                                is_valid = False
                                break
                    except Exception:
                        try:
                            p = sp.poly(f, x_sym, domain='QQ')
                            if p is None:
                                is_valid = False
                                break
                        except Exception:
                            is_valid = False
                            break
                h2 = is_valid
    except Exception:
        h2 = False
        
    try:
        if not h2 or x_sym is None:
            neg_q = False
        else:
            has_monic = contains_monic_of_degree_le_n(I_gens, n, x_sym)
            neg_q = not has_monic
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]
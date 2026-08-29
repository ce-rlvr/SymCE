import sympy
from sympy import Symbol, Rational, Poly, roots, sympify, I, minpoly
from sympy.polys.numberfields import primitive_element
from sympy.abc import x

# Standard algebra objects
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def field_degree(gens):
    unique = []
    for g in gens:
        g = sympify(g)
        if g.is_Rational:
            continue
        try:
            cg = complex(g.evalf())
        except Exception:
            continue
        found = False
        for u in unique:
            if abs(cg - complex(u.evalf())) < 1e-7:
                found = True
                break
        if not found:
            unique.append(g)
    if not unique:
        return 1
    if len(unique) == 1:
        try:
            return minpoly(unique[0], x).degree()
        except Exception:
            return None
    try:
        res = primitive_element(unique, x, ex=False)
        return res[1].degree()
    except Exception:
        try:
            res = primitive_element(unique, x)
            return res[1].degree()
        except Exception:
            return None

def conditions(witness):
    if isinstance(witness, dict):
        F_gens = witness.get('F', [])
        f_expr = witness.get('f', x)
        K_gens = witness.get('K', [])
    else:
        try:
            F_gens, f_expr, K_gens = witness
        except Exception:
            return [False, False, False, False]
    
    if not isinstance(F_gens, (list, tuple)):
        F_gens = [F_gens]
    if not isinstance(K_gens, (list, tuple)):
        K_gens = [K_gens]
        
    # H1: F is a field
    h1_ok = isinstance(F_gens, (list, tuple))
    
    # H2: f(x) is a separable polynomial
    try:
        poly_f = Poly(f_expr, x)
        deg_f = poly_f.degree()
        rts = roots(f_expr, x)
        if deg_f < 1 or sum(rts.values()) != deg_f:
            h2_ok = False
        else:
            h2_ok = all(mult == 1 for mult in rts.values())
    except Exception:
        h2_ok = False
        
    # H3: K is the splitting field of f(x) over F
    try:
        if h2_ok:
            roots_list = list(rts.keys())
            deg_K = field_degree(K_gens)
            deg_F_roots = field_degree(list(F_gens) + roots_list)
            deg_K_F_roots = field_degree(list(K_gens) + list(F_gens) + roots_list)
            if deg_K is not None and deg_F_roots is not None and deg_K_F_roots is not None:
                h3_ok = (deg_K == deg_F_roots) and (deg_K == deg_K_F_roots)
            else:
                h3_ok = False
        else:
            h3_ok = False
    except Exception:
        h3_ok = False
        
    # neg_Q: K/F is not Galois
    is_galois = None
    try:
        deg_K = field_degree(K_gens)
        deg_F = field_degree(F_gens)
        all_gens = list(F_gens) + list(K_gens)
        deg_K_F_ext = field_degree(all_gens)
        
        if deg_K is None or deg_F is None or deg_K_F_ext != deg_K or deg_K % deg_F != 0:
            is_galois = False
        else:
            deg_K_F = deg_K // deg_F
            
            unique_gens = []
            gen_mapping = []
            for g in all_gens:
                g = sympify(g)
                if g.is_Rational:
                    gen_mapping.append(-1)
                    continue
                try:
                    cg = complex(g.evalf())
                except Exception:
                    cg = 0
                found = False
                for j, u in enumerate(unique_gens):
                    if abs(cg - complex(u.evalf())) < 1e-7:
                        gen_mapping.append(j)
                        found = True
                        break
                if not found:
                    gen_mapping.append(len(unique_gens))
                    unique_gens.append(g)
            
            if not unique_gens:
                is_galois = True
            else:
                res = primitive_element(unique_gens, x, ex=True)
                elem = res[0]
                minp = res[1]
                morphisms = res[2]
                
                roots_K = roots(minp, x)
                if sum(roots_K.values()) == minp.degree():
                    aut_count = 0
                    for r in roots_K.keys():
                        if field_degree([elem, r]) == minp.degree():
                            fixes_F = True
                            for i in range(len(F_gens)):
                                idx = gen_mapping[i]
                                if idx == -1:
                                    continue
                                poly_expr = morphisms[idx]
                                if hasattr(poly_expr, 'as_expr'):
                                    poly_expr = poly_expr.as_expr()
                                val_r = poly_expr.subs(x, r)
                                val_orig = all_gens[i]
                                if abs(complex(val_r.evalf()) - complex(sympify(val_orig).evalf())) > 1e-7:
                                    fixes_F = False
                                    break
                            if fixes_F:
                                aut_count += 1
                    is_galois = (aut_count == deg_K_F)
    except Exception:
        pass
        
    if is_galois is not None:
        neg_Q_ok = not is_galois
    else:
        neg_Q_ok = False
        
    return [h1_ok, h2_ok, h3_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a separable polynomial",
    "H_3: K is the splitting field of f(x) over F",
    "¬Q: The field extension K/F is not a Galois extension"
]

N_HYP = 3
NEG_Q_INDEX = 3
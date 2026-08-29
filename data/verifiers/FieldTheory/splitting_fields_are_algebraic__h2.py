import sympy
from sympy import QQ, Symbol, pi, E, I, sqrt, Poly, Rational, Integer

x = Symbol('x')
y = Symbol('y')
z = Symbol('z')

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: E is a splitting field of S over F",
    "¬Q: Not every element of E is algebraic over F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1, h2, neg_q = False, False, False

    try:
        if isinstance(witness, dict):
            F = witness.get('F', None)
            E = witness.get('E', None)
            E_gens = witness.get('E_gens', None)
            S = witness.get('S', [])
            var = witness.get('var', None)
            S_roots = witness.get('S_roots', None)
            non_alg_elem = witness.get('non_alg_elem', None)
        elif isinstance(witness, tuple) and len(witness) == 3:
            F, E, S = witness
            E_gens = None
            var = None
            S_roots = None
            non_alg_elem = None
        else:
            return [False, False, False]

        # H1: F is a field
        if hasattr(F, 'is_Field') and F.is_Field:
            h1 = True
        elif F == sympy.QQ:
            h1 = True

        # Determine E_gens if not provided
        if E_gens is None:
            if hasattr(E, 'gens'):
                E_gens = list(E.gens)
            elif hasattr(E, 'ext'):
                ext = E.ext
                if hasattr(ext, 'as_expr'):
                    E_gens = [ext.as_expr()]
                elif hasattr(ext, 'expr'):
                    E_gens = [ext.expr]
                else:
                    E_gens = [ext]
            else:
                E_gens = []

        # Normalize S to expressions
        S_exprs = []
        for p in S:
            if hasattr(p, 'as_expr'):
                S_exprs.append(p.as_expr())
            elif isinstance(p, sympy.Expr):
                S_exprs.append(p)
            else:
                S_exprs.append(sympy.sympify(p))
        S = S_exprs

        # Determine var if not provided
        if var is None:
            all_symbols = set()
            for p in S:
                if hasattr(p, 'free_symbols'):
                    all_symbols.update(p.free_symbols)
            E_gen_symbols = set()
            for g in E_gens:
                if hasattr(g, 'free_symbols'):
                    E_gen_symbols.update(g.free_symbols)
            vars = all_symbols - E_gen_symbols
            if len(vars) == 1:
                var = list(vars)[0]
            elif len(vars) == 0:
                var = list(all_symbols)[0] if all_symbols else sympy.Symbol('y')
            else:
                var = list(vars)[0]

        # H2: E is a splitting field of S over F
        splits_completely = True
        all_roots = set()
        
        if S_roots is not None:
            for p, roots in zip(S, S_roots):
                all_roots.update(roots)
                if len(roots) != sympy.degree(p, var):
                    splits_completely = False
                for r in roots:
                    if sympy.simplify(p.subs(var, r)) != 0:
                        splits_completely = False
        else:
            for p in S:
                rts = sympy.roots(p, var)
                deg = sympy.degree(p, var)
                if sum(rts.values()) != deg or deg == 0:
                    splits_completely = False
                    break
                all_roots.update(rts.keys())
        
        if splits_completely:
            roots_in_E = True
            if hasattr(E, 'from_sympy'):
                for r in all_roots:
                    try:
                        if E.from_sympy(r) is None:
                            roots_in_E = False
                            break
                    except Exception:
                        roots_in_E = False
                        break
            elif E_gens:
                for r in all_roots:
                    try:
                        sym_gens = [g for g in E_gens if isinstance(g, sympy.Symbol)]
                        if sym_gens:
                            if hasattr(r, 'is_rational_function') and not r.is_rational_function(*sym_gens):
                                roots_in_E = False
                                break
                    except Exception:
                        pass

            if roots_in_E:
                generated = False
                if hasattr(F, 'frac_field'):
                    try:
                        gens = [r for r in all_roots if not (hasattr(r, 'is_Rational') and r.is_Rational)]
                        if not gens:
                            if E == F:
                                generated = True
                        else:
                            gen_field = F.frac_field(*gens)
                            if E == gen_field:
                                generated = True
                    except Exception:
                        pass
                
                if not generated and hasattr(F, 'algebraic_field'):
                    try:
                        gens = [r for r in all_roots if not (hasattr(r, 'is_Rational') and r.is_Rational)]
                        if gens:
                            gen_field = F.algebraic_field(*gens)
                            if E == gen_field:
                                generated = True
                    except Exception:
                        pass

                if generated:
                    h2 = True
                else:
                    root_symbols = set()
                    for r in all_roots:
                        if hasattr(r, 'free_symbols'):
                            root_symbols.update(r.free_symbols)
                    
                    E_gen_symbols = set()
                    for g in E_gens:
                        if hasattr(g, 'free_symbols'):
                            E_gen_symbols.update(g.free_symbols)
                    
                    if root_symbols == E_gen_symbols and len(root_symbols) > 0:
                        h2 = True

        # neg_Q: Not every element of E is algebraic over F
        if non_alg_elem is None and E_gens:
            F_gens = set()
            if hasattr(F, 'gens'):
                for g in F.gens:
                    if hasattr(g, 'free_symbols'):
                        F_gens.update(g.free_symbols)
            
            for g in E_gens:
                g_syms = set()
                if hasattr(g, 'free_symbols'):
                    g_syms.update(g.free_symbols)
                if not g_syms.issubset(F_gens):
                    non_alg_elem = g
                    break
            
            if non_alg_elem is None:
                for g in E_gens:
                    if getattr(g, 'is_algebraic', None) is False:
                        non_alg_elem = g
                        break

        if non_alg_elem is not None:
            F_gens = set()
            if hasattr(F, 'gens'):
                for g in F.gens:
                    if hasattr(g, 'free_symbols'):
                        F_gens.update(g.free_symbols)
            
            elem_syms = set()
            if hasattr(non_alg_elem, 'free_symbols'):
                elem_syms.update(non_alg_elem.free_symbols)
            
            if not elem_syms.issubset(F_gens):
                neg_q = True
            elif getattr(non_alg_elem, 'is_algebraic', None) is False:
                neg_q = True

    except Exception:
        pass

    return [bool(h1), bool(h2), bool(neg_q)]
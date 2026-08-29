import sympy
from sympy import Matrix, sympify

# Top-level setup: named object bindings that the witness expression may reference.
u, v, w, x, y, z, t = sympy.symbols('u v w x y z t')

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: K_bar is the algebraic closure of K within L",
    "H_2: S is a subset of L",
    "¬Q: Algebraic independence of S over K is not equivalent to algebraic independence over K_bar"
]

def conditions(witness):
    try:
        def get_list(name):
            if isinstance(witness, dict):
                val = witness.get(name, [])
            else:
                val = getattr(witness, name, [])
            if not isinstance(val, (list, tuple, set)):
                val = [val]
            return list(val)

        K_list = get_list('K')
        L_list = get_list('L')
        K_bar_list = get_list('K_bar')
        S_list = get_list('S')

        def trdeg(exprs):
            if not exprs:
                return 0
            syms = set()
            parsed_exprs = []
            for e in exprs:
                e_sym = sympify(e)
                parsed_exprs.append(e_sym)
                if hasattr(e_sym, 'free_symbols'):
                    syms.update(e_sym.free_symbols)
            syms = list(syms)
            if not syms:
                return 0
            # Compute Jacobian matrix to find transcendence degree
            J = Matrix([[sympy.cancel(sympy.diff(e, s)) for s in syms] for e in parsed_exprs])
            return J.rank()

        trdeg_K = trdeg(K_list)

        # H1: K_bar is the algebraic closure of K within L
        expected_K_bar = []
        for val in L_list:
            if trdeg(K_list + [val]) == trdeg_K:
                expected_K_bar.append(val)
        
        def unique_exprs(exprs):
            res = []
            for e in exprs:
                found = False
                for r in res:
                    if sympy.cancel(sympify(e) - sympify(r)) == 0:
                        found = True
                        break
                if not found:
                    res.append(e)
            return res

        K_bar_unique = unique_exprs(K_bar_list)
        expected_K_bar_unique = unique_exprs(expected_K_bar)

        def expr_set_eq(set1, set2):
            if len(set1) != len(set2):
                return False
            for e1 in set1:
                found = False
                for e2 in set2:
                    if sympy.cancel(sympify(e1) - sympify(e2)) == 0:
                        found = True
                        break
                if not found:
                    return False
            return True

        h1 = expr_set_eq(K_bar_unique, expected_K_bar_unique)

        # H2: S is a subset of L
        h2 = True
        for s_val in S_list:
            found = False
            for l_val in L_list:
                if sympy.cancel(sympify(s_val) - sympify(l_val)) == 0:
                    found = True
                    break
            if not found:
                h2 = False
                break

        # Conclusion: S is algebraically independent over K iff S is algebraically independent over K_bar
        S_unique = unique_exprs(S_list)
                
        indep_K = (trdeg(K_list + S_unique) - trdeg_K == len(S_unique))
        
        trdeg_K_bar = trdeg(K_bar_list)
        indep_K_bar = (trdeg(K_bar_list + S_unique) - trdeg_K_bar == len(S_unique))
        
        q = (indep_K == indep_K_bar)
        neg_q = not q
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]
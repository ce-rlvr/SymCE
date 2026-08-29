import sympy as sp
import z3
import itertools

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def is_non_degenerate_symbolic(B, V_dim):
    u = [z3.Real(f'u{i}') for i in range(V_dim)]
    v = [z3.Real(f'v{i}') for i in range(V_dim)]
    
    try:
        B_uv = B(u, v)
    except Exception:
        return None
        
    try:
        # Check left degeneracy
        solver = z3.Solver()
        u_nonzero = z3.Or([ui != 0 for ui in u])
        solver.add(u_nonzero)
        solver.add(z3.ForAll(v, B_uv == 0))
        solver.set("timeout", 2000)
        res_left = solver.check()
        
        if res_left == z3.sat:
            return False
            
        # Check right degeneracy
        solver = z3.Solver()
        v_nonzero = z3.Or([vi != 0 for vi in v])
        solver.add(v_nonzero)
        solver.add(z3.ForAll(u, B_uv == 0))
        solver.set("timeout", 2000)
        res_right = solver.check()
        
        if res_right == z3.sat:
            return False
            
        if res_left == z3.unsat and res_right == z3.unsat:
            return True
    except Exception:
        return None
        
    return None

def conditions(witness):
    try:
        V_dim = witness['V_dim']
        B = witness['B']
        M = sp.Matrix(witness['M'])
    except Exception:
        return [False, False, False, False]
        
    # H1: V is a finite-dimensional vector space
    try:
        h1 = isinstance(V_dim, int) and V_dim > 0
        if 'field' in witness:
            h1 = h1 and sp.isprime(witness['field'])
    except Exception:
        h1 = False
        
    # H2: E is a basis for V
    # We implicitly use the standard basis, so this holds if V is valid.
    h2 = h1
    
    # H3: M is the Gram matrix of B with respect to the basis E
    try:
        h3 = True
        if 'field' in witness:
            p = witness['field']
            for i in range(V_dim):
                for j in range(V_dim):
                    e_i = [0]*V_dim; e_i[i] = 1
                    e_j = [0]*V_dim; e_j[j] = 1
                    if int(M[i, j]) % p != int(B(e_i, e_j)) % p:
                        h3 = False
                        break
        else:
            for i in range(V_dim):
                for j in range(V_dim):
                    e_i = [0]*V_dim; e_i[i] = 1
                    e_j = [0]*V_dim; e_j[j] = 1
                    if sp.simplify(M[i, j] - B(e_i, e_j)) != 0:
                        h3 = False
                        break
    except Exception:
        h3 = False
        
    # Conclusion: B is non-degenerate if and only if the determinant of M is non-zero
    try:
        if 'field' in witness:
            p = witness['field']
            vectors = list(itertools.product(range(p), repeat=V_dim))
            
            left_non_deg = True
            for u in vectors:
                if all(x == 0 for x in u): continue
                if all(int(B(u, v)) % p == 0 for v in vectors):
                    left_non_deg = False
                    break
                    
            right_non_deg = True
            for v in vectors:
                if all(x == 0 for x in v): continue
                if all(int(B(u, v)) % p == 0 for u in vectors):
                    right_non_deg = False
                    break
                    
            is_non_deg = left_non_deg and right_non_deg
            det_nonzero = (int(M.det()) % p) != 0
            neg_q = (is_non_deg != det_nonzero)
        else:
            det_nonzero = sp.simplify(M.det()) != 0
            is_non_deg = is_non_degenerate_symbolic(B, V_dim)
            
            if is_non_deg is None:
                is_degenerate = False
                if 'degenerate_u' in witness:
                    u = witness['degenerate_u']
                    if not all(c == 0 for c in u):
                        v_sym = list(sp.symbols(f'v0:{V_dim}'))
                        expr = B(u, v_sym)
                        if sp.simplify(expr) == 0:
                            is_degenerate = True
                if 'degenerate_v' in witness:
                    v = witness['degenerate_v']
                    if not all(c == 0 for c in v):
                        u_sym = list(sp.symbols(f'u0:{V_dim}'))
                        expr = B(u_sym, v)
                        if sp.simplify(expr) == 0:
                            is_degenerate = True
                            
                if is_degenerate:
                    is_non_deg = False
                    
            if is_non_deg is not None:
                neg_q = bool(is_non_deg != det_nonzero)
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "H_2: E is a basis for V",
    "H_3: M is the Gram matrix of B with respect to the basis E",
    "¬Q: B is non-degenerate if and only if the determinant of M is non-zero fails"
]

N_HYP = 3
NEG_Q_INDEX = 3
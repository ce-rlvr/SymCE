import sympy
import itertools
from sympy import eye, zeros

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be provided as:
      - A tuple (T_func, v) where T_func is a callable or a sympy Matrix, and v is a list/tuple.
      - A tuple (T_expr, v, vars) where T_expr is a list of sympy expressions, v is a list/tuple, 
        and vars is a list/tuple of sympy symbols.
    """
    try:
        if len(witness) == 2:
            T_obj, v = witness
            n = len(v)
            if n == 0:
                return [False, False, False]
            vars = sympy.symbols(f'x0:{n}')
            if callable(T_obj):
                T_expr = T_obj(vars)
            elif isinstance(T_obj, sympy.Matrix):
                T_expr = list(T_obj * sympy.Matrix(vars))
            else:
                return [False, False, False]
        elif len(witness) == 3:
            T_expr, v, vars = witness
            n = len(v)
            if n == 0:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(T_expr, sympy.Matrix):
            T_expr = list(T_expr)
        else:
            T_expr = list(T_expr)
            
        if isinstance(v, sympy.Matrix):
            v = list(v)
        else:
            v = list(v)
    except Exception:
        return [False, False, False]
        
    # H_1: V is a finite-dimensional vector space over a field F
    try:
        h1_ok = True
    except Exception:
        h1_ok = False
        
    # H_2: There exists v in V such that {v, Tv, ..., T^{n-1}v} forms a basis for V
    try:
        basis_vectors = []
        curr_v = v
        for _ in range(n):
            basis_vectors.append(curr_v)
            subs_dict = {vars[i]: curr_v[i] for i in range(n)}
            next_v = [sympy.simplify(expr.subs(subs_dict)) for expr in T_expr]
            curr_v = next_v
        M = sympy.Matrix(basis_vectors)
        h2_ok = bool(sympy.simplify(M.det()) != 0)
    except Exception:
        h2_ok = False
        
    # ¬Q: There does NOT exist a linear functional f in V^* such that {f, T^*f, ..., (T^*)^{n-1}f} forms a basis for V^*
    try:
        # Compute T^{(k)}(x) for k = 0 to n-1
        T_k = [list(vars)]
        curr_T = list(T_expr)
        for _ in range(1, n):
            T_k.append(curr_T)
            next_T = []
            for expr in T_expr:
                subs_dict = {vars[i]: curr_T[i] for i in range(n)}
                next_T.append(sympy.simplify(expr.subs(subs_dict)))
            curr_T = next_T
            
        C = []
        J = []
        Rem = []
        for k in range(n):
            C_k = []
            J_k = []
            Rem_k = []
            for i in range(n):
                expr = T_k[k][i]
                c_val = expr.subs({v_var: 0 for v_var in vars})
                C_k.append(c_val)
                
                j_row = []
                for j in range(n):
                    j_val = sympy.diff(expr, vars[j]).subs({v_var: 0 for v_var in vars})
                    j_row.append(j_val)
                J_k.append(j_row)
                
                rem = expr - c_val
                for j in range(n):
                    rem -= j_row[j] * vars[j]
                Rem_k.append(sympy.simplify(rem))
            C.append(C_k)
            J.append(sympy.Matrix(J_k))
            Rem.append(Rem_k)
            
        # Build the linear system E * c^T = 0 to enforce that f(T^k(x)) is a linear functional
        E_rows = []
        for k in range(1, n):
            E_rows.append(C[k])
            
            monomial_to_row = {}
            is_poly = True
            for i in range(n):
                rem_expr = sympy.expand(Rem[k][i])
                if rem_expr == 0:
                    continue
                try:
                    poly = sympy.Poly(rem_expr, *vars)
                    for monom, coeff in poly.terms():
                        if monom not in monomial_to_row:
                            monomial_to_row[monom] = [0]*n
                        monomial_to_row[monom][i] = coeff
                except Exception:
                    is_poly = False
                    break
            
            if is_poly:
                for row in monomial_to_row.values():
                    E_rows.append(row)
            else:
                pts = list(itertools.product([0, 1, -1], repeat=n))
                for pt in pts[:20]:
                    subs_dict = {vars[j]: pt[j] for j in range(n)}
                    row = [Rem[k][j].subs(subs_dict) for j in range(n)]
                    E_rows.append(row)
                    
        if not E_rows:
            E = sympy.zeros(1, n)
        else:
            E = sympy.Matrix(E_rows)
            
        try:
            E = E.applyfunc(sympy.nsimplify)
        except Exception:
            pass
            
        null_space = E.nullspace()
        
        if not null_space:
            neg_q_ok = True
        else:
            # Parameterize the null space
            t_vars = sympy.symbols(f't0:{len(null_space)}')
            c = sympy.zeros(1, n)
            for idx, vec in enumerate(null_space):
                c += t_vars[idx] * vec.T
                
            # Construct the matrix M whose rows are the coefficient vectors of f(T^k(x))
            M_rows = []
            for k in range(n):
                row_k = c * J[k]
                M_rows.append(list(row_k))
                
            M_matrix = sympy.Matrix(M_rows)
            det_M = sympy.simplify(M_matrix.det())
            
            # If the determinant is identically zero, no such f exists
            if det_M == 0:
                neg_q_ok = True
            else:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: There exists v in V such that {v, Tv, ..., T^{n-1}v} forms a basis for V",
    "¬Q: There does NOT exist a linear functional f in V^* such that {f, T^*f, ..., (T^*)^{n-1}f} forms a basis for V^*"
]

N_HYP = 2
NEG_Q_INDEX = 2
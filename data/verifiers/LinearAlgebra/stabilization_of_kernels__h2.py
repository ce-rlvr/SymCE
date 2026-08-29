import sympy
import itertools

# Top-level setup
x, y, z = sympy.symbols('x y z')
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        neg_q = False
        
        # Case 1: Witness is a SymPy expression (non-linear operator on C^n)
        if isinstance(witness, sympy.Expr) or (isinstance(witness, (list, tuple)) and all(isinstance(e, sympy.Expr) for e in witness)):
            if isinstance(witness, sympy.Expr):
                exprs = [witness]
            else:
                exprs = list(witness)
                
            n = len(exprs)
            free_syms = set()
            for e in exprs:
                free_syms.update(e.free_symbols)
                
            vars = sorted(list(free_syms), key=lambda s: s.name)
            if len(vars) > n:
                return [False, False]
                
            default_syms = sympy.symbols('x y z t u v w')
            idx = 0
            while len(vars) < n:
                if default_syms[idx] not in vars:
                    vars.append(default_syms[idx])
                idx += 1
                
            h1 = True
            
            def get_ker_expr(k):
                if k == 0:
                    return {(0,) * n}
                Tk = exprs
                for _ in range(k - 1):
                    Tk = [e.subs(zip(vars, Tk)) for e in exprs]
                sols = sympy.solve(Tk, vars, dict=True)
                ker = set()
                for sol in sols:
                    tup = tuple(sympy.simplify(sol.get(v, v)) for v in vars)
                    ker.add(tup)
                return ker

            kers = []
            for k in range(n + 2):
                kers.append(get_ker_expr(k))
                
            q = False
            for k in range(n + 1):
                if kers[k] == kers[k+1]:
                    q = True
                    break
            neg_q = not q
            return [h1, neg_q]

        # Case 2: Witness is a dictionary (operator on a finite set)
        elif isinstance(witness, dict):
            keys = list(witness.keys())
            if not keys:
                return [False, False]
            
            if all(isinstance(k, tuple) for k in keys):
                n = len(keys[0])
                zero = tuple([0]*n)
            elif all(isinstance(k, int) for k in keys):
                n = 1
                zero = 0
            else:
                return [False, False]
                
            if zero not in witness:
                return [False, False]
                
            if not all(v in witness for v in witness.values()):
                return [False, False]
                
            h1 = True
            
            def get_ker_dict(k):
                ker = set()
                for v in keys:
                    curr = v
                    for _ in range(k):
                        curr = witness[curr]
                    if curr == zero:
                        ker.add(v)
                return ker
                
            kers = []
            for k in range(n + 2):
                kers.append(get_ker_dict(k))
                
            q = False
            for k in range(n + 1):
                if kers[k] == kers[k+1]:
                    q = True
                    break
            neg_q = not q
            return [h1, neg_q]

        # Case 3: Witness is a tuple (Matrix, mod) (linear operator over a finite ring)
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], sympy.Matrix) and isinstance(witness[1], int):
            mat, mod = witness
            if not mat.is_square:
                return [False, False]
            n = mat.shape[0]
            h1 = True
            
            elements = list(itertools.product(range(mod), repeat=n))
            
            def get_ker_mod(k):
                ker = set()
                if k == 0:
                    Tk = sympy.eye(n)
                else:
                    Tk = (mat**k).applyfunc(lambda val: val % mod)
                for v in elements:
                    v_mat = sympy.Matrix(v)
                    res = (Tk * v_mat).applyfunc(lambda val: val % mod)
                    if all(val == 0 for val in res):
                        ker.add(v)
                return ker
                
            kers = []
            for k in range(n + 2):
                kers.append(get_ker_mod(k))
                
            q = False
            for k in range(n + 1):
                if kers[k] == kers[k+1]:
                    q = True
                    break
            neg_q = not q
            return [h1, neg_q]

        # Case 4: Witness is a SymPy Matrix (linear operator over a field)
        elif isinstance(witness, sympy.Matrix):
            if not witness.is_square:
                return [False, False]
            n = witness.shape[0]
            h1 = True
            
            def get_ker_mat(k):
                if k == 0:
                    Tk = sympy.eye(n)
                else:
                    Tk = witness**k
                ns = Tk.nullspace()
                if not ns:
                    return sympy.Matrix([])
                return sympy.Matrix([v.T for v in ns]).rref()[0]
                
            kers = []
            for k in range(n + 2):
                kers.append(get_ker_mat(k))
                
            q = False
            for k in range(n + 1):
                if kers[k] == kers[k+1]:
                    q = True
                    break
            neg_q = not q
            return [h1, neg_q]

        return [False, False]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space",
    "¬Q: ker(T^k) does not stabilize within dim(V) steps"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import itertools

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If T: U -> V is a linear transformation and rank(T), rank(S) are finite, 
    then rank(S \circ T) <= min(rank(S), rank(T))."
    (The dropped hypothesis is that S is a linear transformation).
    
    Expected witness format:
    (T_matrix, S_exprs, vars)
      - T_matrix: a sympy Matrix representing the linear map T: F^n -> F^m
      - S_exprs: a list of sympy expressions (or a callable) representing the map S: F^m -> F^k
      - vars: a tuple of sympy symbols of length m (or an integer m if S_exprs is callable)
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
            
        T_matrix, S_exprs, vars = witness
        
        # Simple deterministic LCG to generate evaluation points
        def generate_points(dim, count):
            state = 12345
            pts = []
            for _ in range(count):
                pt = []
                for _ in range(dim):
                    state = (1103515245 * state + 12345) % 2147483648
                    pt.append((state % 21) - 10)
                pts.append(pt)
            return pts

        if callable(S_exprs):
            S_func = S_exprs
            if isinstance(vars, int):
                m = vars
            else:
                m = len(vars)
                
            h1 = (isinstance(T_matrix, sympy.Matrix) and 
                  T_matrix.shape[0] == m and
                  m > 0 and T_matrix.shape[1] > 0)
            h2 = isinstance(T_matrix, sympy.Matrix)
            if not (h1 and h2):
                return [False, False, False, False]
                
            rank_T = T_matrix.rank()
            
            pts_S = generate_points(m, 50)
            S_images = []
            for pt in pts_S:
                res = S_func(pt)
                if isinstance(res, (int, float, sympy.Basic)):
                    res = [res]
                elif not isinstance(res, (list, tuple)):
                    res = list(res)
                S_images.append(list(res))
            rank_S = sympy.Matrix(S_images).rank()
            
            n = T_matrix.shape[1]
            pts_T = generate_points(n, 50)
            ST_images = []
            for pt in pts_T:
                T_pt = T_matrix * sympy.Matrix(pt)
                res = S_func(list(T_pt))
                if isinstance(res, (int, float, sympy.Basic)):
                    res = [res]
                elif not isinstance(res, (list, tuple)):
                    res = list(res)
                ST_images.append(list(res))
            rank_ST = sympy.Matrix(ST_images).rank()
            
        else:
            if isinstance(S_exprs, sympy.Matrix):
                S_exprs = list(S_exprs)
                
            h1 = (isinstance(T_matrix, sympy.Matrix) and 
                  isinstance(vars, (list, tuple)) and 
                  T_matrix.shape[0] == len(vars) and
                  len(vars) > 0 and T_matrix.shape[1] > 0)
            h2 = isinstance(T_matrix, sympy.Matrix)
            if not (h1 and h2):
                return [False, False, False, False]
                
            rank_T = T_matrix.rank()
            
            m = len(vars)
            pts_S = generate_points(m, max(50, len(S_exprs) + 10))
            S_images = []
            for pt in pts_S:
                val = [sympy.sympify(e).subs(zip(vars, pt)) for e in S_exprs]
                S_images.append(val)
            rank_S = sympy.Matrix(S_images).rank()
            
            n = T_matrix.shape[1]
            pts_T = generate_points(n, max(50, len(S_exprs) + 10))
            ST_images = []
            for pt in pts_T:
                T_pt = T_matrix * sympy.Matrix(pt)
                val = [sympy.sympify(e).subs(zip(vars, T_pt)) for e in S_exprs]
                ST_images.append(val)
            rank_ST = sympy.Matrix(ST_images).rank()
            
        h3 = (isinstance(rank_T, int) and isinstance(rank_S, int))
        
        neg_q = rank_ST > min(rank_S, rank_T)
        
        return [h1, h2, h3, neg_q]
        
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: U, V, and W are vector spaces over a field F",
    "H_2: T: U -> V is a linear transformation",
    "H_3: rank(T) and rank(S) are finite",
    "¬Q: rank(S \\circ T) > min(rank(S), rank(T))"
]

N_HYP = 3
NEG_Q_INDEX = 3
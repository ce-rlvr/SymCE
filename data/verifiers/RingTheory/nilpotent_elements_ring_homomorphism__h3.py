import sympy as sp
from sympy import Matrix, eye, zeros

# Top-level setup for standard rings and matrices
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)
Z = sp.S.Integers
Q = sp.S.Rationals

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Format 1: Integer, Float, or SymPy Number (Implicitly R=Z, S=Z, f=id)
        if isinstance(witness, (int, float)) or isinstance(witness, sp.Number):
            h1 = True
            h2 = True
            # In Z, the only nilpotent element is 0
            neg_q = (witness != 0)
            return [h1, h2, neg_q]
            
        # Format 2: Matrix (Implicitly R=M_n, S=M_n, f=id)
        if isinstance(witness, Matrix):
            h1 = True
            h2 = True
            if witness.shape[0] == witness.shape[1]:
                n = witness.shape[0]
                is_nilp = (witness**n == zeros(n, n))
                neg_q = not is_nilp
            return [h1, h2, neg_q]
            
        # Format 3 & 4: Tuple/List of length 4 -> (R, S, f, x)
        if isinstance(witness, (tuple, list)) and len(witness) == 4:
            R_obj, S_obj, f, x = witness
            
            # Sub-format 3: Z/nZ -> Z/mZ
            if isinstance(R_obj, int) and isinstance(S_obj, int):
                n, m = R_obj, S_obj
                if n > 0 and m > 0:
                    h1 = True
                
                if h1 and isinstance(f, (dict, list, tuple)):
                    h2 = True
                    for i in range(n):
                        val = f[i] if isinstance(f, dict) else (f[i] if i < len(f) else None)
                        if val is None or not isinstance(val, int):
                            h2 = False
                            break
                    if h2:
                        f_map = f
                        if f_map[1 % n] % m != 1 % m:
                            h2 = False
                        else:
                            for a in range(n):
                                for b in range(n):
                                    fa = f_map[a]
                                    fb = f_map[b]
                                    if f_map[(a + b) % n] % m != (fa + fb) % m:
                                        h2 = False
                                        break
                                    if f_map[(a * b) % n] % m != (fa * fb) % m:
                                        h2 = False
                                        break
                                if not h2:
                                    break
                
                if h1 and h2:
                    fx = f[x] % m if isinstance(f, dict) else f[x] % m
                    if m == 1:
                        neg_q = False
                    else:
                        curr = fx
                        is_nilp = False
                        for _ in range(m):
                            if curr == 0:
                                is_nilp = True
                                break
                            curr = (curr * fx) % m
                        neg_q = not is_nilp
                return [h1, h2, neg_q]
                
            # Sub-format 4: General objects
            else:
                h1 = True # Assume they are rings if provided as objects
                if callable(f):
                    try:
                        if f(1) == 1 and f(2+3) == f(2)+f(3) and f(2*3) == f(2)*f(3):
                            h2 = True
                    except Exception:
                        pass
                elif isinstance(f, dict):
                    h2 = True
                
                try:
                    if callable(f):
                        fx = f(x)
                        h2 = True
                    elif isinstance(f, dict):
                        fx = f[x]
                    else:
                        fx = x # fallback to identity
                        h2 = True
                        
                    if isinstance(fx, (int, float)) or isinstance(fx, sp.Number):
                        neg_q = (fx != 0)
                    elif isinstance(fx, Matrix):
                        n_dim = fx.shape[0]
                        neg_q = (fx**n_dim != zeros(n_dim, n_dim))
                    else:
                        curr = fx
                        is_nilp = False
                        for _ in range(10):
                            if curr == 0:
                                is_nilp = True
                                break
                            curr = curr * fx
                        neg_q = not is_nilp
                except Exception:
                    neg_q = False
                    
                return [h1, h2, neg_q]
                
        # Format 5: Tuple/List of length 2 -> (f, x)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            f, x = witness
            h1 = True
            if callable(f):
                try:
                    if f(1) == 1 and f(2+3) == f(2)+f(3) and f(2*3) == f(2)*f(3):
                        h2 = True
                    fx = f(x)
                except Exception:
                    h2 = False
                    fx = x
            else:
                h2 = False
                fx = x
            
            if h1 and h2:
                if isinstance(fx, (int, float)) or isinstance(fx, sp.Number):
                    neg_q = (fx != 0)
                elif isinstance(fx, Matrix):
                    n_dim = fx.shape[0]
                    neg_q = (fx**n_dim != zeros(n_dim, n_dim))
                else:
                    curr = fx
                    is_nilp = False
                    for _ in range(10):
                        if curr == 0:
                            is_nilp = True
                            break
                        curr = curr * fx
                    neg_q = not is_nilp
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R and S are rings",
    "H_2: f: R -> S is a ring homomorphism",
    "¬Q: f(x) is not nilpotent in S"
]

N_HYP = 2
NEG_Q_INDEX = 2
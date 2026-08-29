import sympy
from sympy import eye, zeros, Rational, Integer, Matrix
import z3

# Top-level setup: named object bindings
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Every operator T on a finite-dimensional vector space V over an algebraically 
    closed field K has an eigenvalue."
    (The dropped hypothesis is that T must be a LINEAR operator).
    """
    # Default values
    K = 'C'
    n = 2
    T = None
    
    # Parse witness
    if isinstance(witness, dict):
        K = witness.get('K', 'C')
        n = witness.get('V_dim', witness.get('n', 2))
        T = witness.get('T')
    elif isinstance(witness, tuple) and len(witness) == 3:
        K, n, T = witness
    elif callable(witness):
        T = witness
    else:
        T = witness

    # H_1: K is an algebraically closed field
    try:
        h1 = False
        if isinstance(K, str):
            h1 = K.lower() in ['c', 'complexes', 'algebraicallyclosedfield', 'algebraically closed field']
        else:
            if K == sympy.S.Complexes:
                h1 = True
    except Exception:
        h1 = False

    # H_2: V is a finite-dimensional vector space over K of dimension n >= 1
    try:
        if hasattr(T, 'shape') and not callable(T):
            n = T.shape[0]
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False

    # ¬Q: There exists no non-zero vector v in V and scalar lambda in K such that T(v) = lambda v
    # We use z3 to prove that the equation T(v) = lambda * v has no non-zero solutions.
    neg_q = False
    try:
        solver = z3.Solver()
        v_vars = []
        for i in range(n):
            v_vars.append((z3.Real(f'v_r_{i}'), z3.Real(f'v_i_{i}')))
        
        lam_r = z3.Real('lam_r')
        lam_i = z3.Real('lam_i')
        
        # v != 0 constraint
        v_not_zero = z3.Or(*[z3.Or(r != 0, i != 0) for r, i in v_vars])
        solver.add(v_not_zero)
        
        # Evaluate T(v)
        if callable(T):
            T_v = T(v_vars)
        else:
            # Assume T is a matrix-like object (which will always have an eigenvalue over C, 
            # so z3 will return sat and neg_q will correctly be False)
            T_v = []
            for i in range(n):
                row_r = 0
                row_i = 0
                for j in range(n):
                    val = T[i, j] if hasattr(T, 'shape') else T[i][j]
                    val = complex(val)
                    val_r, val_i = val.real, val.imag
                    v_r, v_i = v_vars[j]
                    # Complex multiplication: (val_r + i val_i) * (v_r + i v_i)
                    row_r += val_r * v_r - val_i * v_i
                    row_i += val_r * v_i + val_i * v_r
                T_v.append((row_r, row_i))
                
        # Add T(v) == lambda * v constraints
        for i in range(n):
            T_r, T_i = T_v[i]
            v_r, v_i = v_vars[i]
            
            # lambda * v
            rhs_r = lam_r * v_r - lam_i * v_i
            rhs_i = lam_r * v_i + lam_i * v_r
            
            solver.add(T_r == rhs_r)
            solver.add(T_i == rhs_i)
            
        solver.set("timeout", 4000)
        res = solver.check()
        
        # If unsat, there are NO eigenvectors, meaning the conclusion FAILS (neg_q is True)
        if res == z3.unsat:
            neg_q = True
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: V is a finite-dimensional vector space over K of dimension n >= 1",
    "¬Q: There exists no non-zero vector v in V and scalar lambda in K such that T(v) = lambda v"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)
x = sp.Symbol('x')

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: V is a finite-dimensional vector space over K",
    "H_3: The only eigenvalue of T in K is 0",
    "¬Q: T is not a nilpotent operator"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # The dropped hypothesis is "T is a linear operator".
        # A valid counterexample is a non-linear operator T on V=C over K=C.
        
        # Check if witness is a sympy Matrix (which is linear, so it can't be a counterexample,
        # but we evaluate it for completeness).
        if hasattr(witness, 'eigenvals'):
            K_ok = True
            V_ok = True
            try:
                evals = witness.eigenvals()
                h3 = True
                has_zero = False
                for val in evals.keys():
                    if val == 0:
                        has_zero = True
                    else:
                        h3 = False
                if not has_zero:
                    h3 = False
            except Exception:
                h3 = False
                
            try:
                n = witness.shape[0]
                is_nilp = (witness**n).is_zero_matrix
            except Exception:
                is_nilp = False
                
            neg_q = not is_nilp
            return [K_ok, V_ok, h3, neg_q]
            
        # Check if witness is a sympy expression (representing T(x))
        elif isinstance(witness, sp.Expr):
            free_syms = witness.free_symbols
            if len(free_syms) == 1:
                sym = list(free_syms)[0]
                T = lambda val: witness.subs(sym, val)
            elif len(free_syms) == 0:
                T = lambda val: witness
            else:
                return [False, False, False, False]
            K_ok = True
            V_ok = True
            
        # Check if witness is a callable Python function
        elif callable(witness):
            T = witness
            K_ok = True
            V_ok = True
            
        # Check if witness is a dictionary containing the operator
        elif isinstance(witness, dict):
            T_obj = witness.get('T')
            if callable(T_obj):
                T = T_obj
            elif isinstance(T_obj, sp.Expr):
                free_syms = T_obj.free_symbols
                if len(free_syms) == 1:
                    sym = list(free_syms)[0]
                    T = lambda val: T_obj.subs(sym, val)
                elif len(free_syms) == 0:
                    T = lambda val: T_obj
                else:
                    return [False, False, False, False]
            else:
                return [False, False, False, False]
                
            K_ok = witness.get('K', True) in ['C', 'CC', 'complex', 'algebraically closed', True]
            V_ok = witness.get('V_dim', 1) > 0
            
        else:
            return [False, False, False, False]
            
        # Test values to evaluate the operator's behavior
        test_vals = [1, -1, 1j, -1j, 2+3j, -3.14+2.71j, 0.577+0.618j]
        
        def is_nonzero(val):
            if isinstance(val, sp.Expr):
                if val.is_zero is True:
                    return False
                if val.is_zero is False:
                    return True
                try:
                    return complex(val.evalf()) != 0
                except Exception:
                    return val != 0
            return val != 0

        # H3: The only eigenvalue of T in K is 0.
        # For a non-linear operator, lambda is an eigenvalue if T(x) = lambda * x for some x != 0.
        # If the ONLY eigenvalue is 0, then T(x) MUST be 0 for all x != 0.
        h3 = True
        for val in test_vals:
            if is_nonzero(T(val)):
                h3 = False
                break
                
        # neg_Q: T is not a nilpotent operator.
        # T is nilpotent if there exists n such that T^n(x) == 0 for all x.
        is_nilpotent = False
        for n in range(1, 15):
            all_zero = True
            for val in test_vals + [0]:
                res = val
                for _ in range(n):
                    res = T(res)
                if is_nonzero(res):
                    all_zero = False
                    break
            if all_zero:
                is_nilpotent = True
                break
                
        neg_q = not is_nilpotent
        
        return [bool(K_ok), bool(V_ok), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]
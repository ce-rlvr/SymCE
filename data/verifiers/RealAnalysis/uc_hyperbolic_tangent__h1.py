import sympy
from sympy import Symbol, S, Poly
from sympy.calculus.util import continuous_domain

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness function is NOT uniformly continuous on R.
    Returns [neg_Q], where neg_Q is True if the conclusion fails (i.e., f is NOT uniformly continuous).
    """
    try:
        # Normalize the witness to a sympy expression in terms of x
        if callable(witness):
            f = witness(x)
        else:
            f = witness
            
        if not hasattr(f, 'free_symbols'):
            return [False]
            
        if not f.free_symbols:
            # Constant functions are uniformly continuous
            return [False]
            
        syms = list(f.free_symbols)
        if len(syms) == 1 and syms[0] != x:
            f = f.subs(syms[0], x)
            
    except Exception:
        return [False]

    neg_Q = False

    try:
        # 1. Check if the function is continuous on R
        try:
            dom = continuous_domain(f, x, S.Reals)
            if dom != S.Reals:
                return [True]
        except Exception:
            pass

        # 2. Check if it's a polynomial of degree >= 2
        try:
            p = Poly(f, x)
            if p.degree() >= 2:
                return [True]
        except Exception:
            pass

        # 3. Numerical check for uniform continuity
        # We test a sequence of small, off-beat deltas to avoid aligning with periodic functions.
        deltas = [sympy.Rational(11, 10**k) for k in [3, 5, 7, 9, 11, 13]]
        
        # Limit evaluation range for functions that grow extremely fast to prevent freezing
        has_fast_growth = False
        if f.has(sympy.exp, sympy.sinh, sympy.cosh, sympy.gamma, sympy.factorial):
            has_fast_growth = True
        else:
            for arg in f.atoms(sympy.Pow):
                if arg.exp.has(x):
                    has_fast_growth = True
                    break
                    
        max_base = 10**15
        if has_fast_growth:
            max_base = 1000

        for delta in deltas:
            found_large_diff = False
            
            bases = [0, 1, 10, 100, 1000, 10000, 100000, 1000000, 10**8, 10**10]
            try:
                inv_d = int(1/delta)
                if inv_d <= max_base and inv_d not in bases:
                    bases.append(inv_d)
                if inv_d**2 <= max_base and inv_d**2 not in bases:
                    bases.append(inv_d**2)
            except Exception:
                pass
                
            bases = [b for b in bases if b <= max_base]
            
            for base in bases:
                for offset in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]:
                    for sign in [1, -1]:
                        x_val = sign * (base + offset)
                        try:
                            # Evaluate with high precision to avoid catastrophic cancellation
                            v1 = f.subs(x, x_val).evalf(100)
                            v2 = f.subs(x, x_val + delta).evalf(100)
                            
                            if v1.is_real and v2.is_real:
                                if abs(v1 - v2) > 0.1:
                                    found_large_diff = True
                                    break
                        except Exception:
                            pass
                    if found_large_diff:
                        break
                if found_large_diff:
                    break
                    
            if not found_large_diff:
                # If for any delta we cannot find a difference > 0.1, it is likely uniformly continuous
                return [False]
                
        # If all tested deltas produced a large difference, it is NOT uniformly continuous
        neg_Q = True
        
    except Exception:
        neg_Q = False

    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The function f is not uniformly continuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0
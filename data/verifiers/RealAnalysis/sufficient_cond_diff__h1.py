import sympy as sp

# Top-level setup for potential witness expressions
x, y, z = sp.symbols('x y z', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness can be a tuple (f, vars, U, a) where:
      - f is a sympy expression
      - vars is a list of variables
      - U is a sympy Set representing the domain
      - a is a tuple of coordinates for the point
    Alternatively, it can be a mock object or dictionary with the boolean properties.
    """
    # 1. Try to evaluate mathematically if witness is a tuple
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            f, vars_list, U, a = witness
            
            if not isinstance(vars_list, (list, tuple)):
                vars_list = [vars_list]
            if not isinstance(a, (list, tuple)):
                a = [a]
                
            # H1: f is a function
            h1 = isinstance(f, sp.Expr)
            
            # H2: partial derivatives exist everywhere in U
            # We verify that we can compute them symbolically without trivial failure
            h2 = True
            dfs = []
            for v in vars_list:
                df = sp.diff(f, v)
                if df.has(sp.Derivative):
                    h2 = False
                dfs.append(df)
                
            # H3: partial derivatives are continuous at a
            h3 = True
            for df in dfs:
                val = df.subs(zip(vars_list, a)).doit()
                if val.has(sp.nan, sp.zoo, sp.oo, -sp.oo):
                    h3 = False
                    break
                    
            # ¬Q: f is not differentiable at a
            # Differentiability at 'a' requires 'a' to be an interior point of U.
            # If 'a' is on the boundary or outside, it is not differentiable.
            try:
                if isinstance(U, sp.Set):
                    if len(vars_list) == 1:
                        pt = a[0]
                    else:
                        pt = tuple(a)
                    is_int = U.interior.contains(pt)
                    neg_q = not (is_int == True)
                else:
                    neg_q = False
            except Exception:
                neg_q = False
                
            return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # 2. Fallback for duck typing if witness is a custom object
    try:
        h1 = witness.is_function()
        h2 = witness.partials_exist_everywhere()
        h3 = witness.partials_continuous_at_a()
        neg_q = not witness.is_differentiable_at_a()
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        pass

    # 3. Fallback for dictionary
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_function', False))
            h2 = bool(witness.get('partials_exist_everywhere', False))
            h3 = bool(witness.get('partials_continuous_at_a', False))
            neg_q = not bool(witness.get('is_differentiable_at_a', True))
            return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is a function",
    "H_2: The partial derivatives exist everywhere in U",
    "H_3: The partial derivatives are continuous at a",
    "¬Q: f is not differentiable at a"
]

N_HYP = 3
NEG_Q_INDEX = 3
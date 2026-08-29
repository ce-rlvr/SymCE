import sympy

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x')
t1, t2, t3, t4, t5, t6, t7, t8, t9, t10 = sympy.symbols('t1:11')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    Expected witness format: tuple (n, f)
      - n: an integer >= 1 (representing the number of variables t_1, ..., t_n)
      - f: a sympy expression representing a polynomial in x over K = Q(t_1, ..., t_n)
    """
    try:
        n, f = witness
    except Exception:
        return [False, False, False, False, False]
    
    # H_1: F is a field (we implicitly use F = Q, which is a field)
    h1 = True
    
    # H_2: t_1, ..., t_n are algebraically independent variables over F
    try:
        h2 = isinstance(n, int) and n >= 1
    except Exception:
        h2 = False
        
    # H_3: K = F(t_1, ..., t_n) is the field of rational functions
    h3 = True
    
    # H_4: E is the splitting field of f(x) over K
    # This holds as long as f(x) is a valid polynomial in x.
    try:
        sympy.Poly(f, x)
        h4 = True
    except Exception:
        h4 = False
        
    # ¬Q: The Galois group Gal(E/K) is not isomorphic to S_n
    try:
        neg_q = False
        if h2 and h4:
            d = sympy.degree(f, x)
            try:
                d = int(d)
            except TypeError:
                d = -1  # Handle cases like degree(0, x) which is -oo
                
            if n >= 2:
                # If degree < n, the Galois group is a subgroup of S_d, so its order divides d! < n!
                if d < n:
                    neg_q = True
                # If degree == n but f is reducible over K, the Galois group cannot be S_n
                elif d == n:
                    factored = sympy.factor(f)
                    if isinstance(factored, sympy.Mul):
                        x_factors = [arg for arg in factored.args if x in arg.free_symbols]
                        if len(x_factors) > 1:
                            neg_q = True
                    elif isinstance(factored, sympy.Pow):
                        if x in factored.base.free_symbols and factored.exp > 1:
                            neg_q = True
            elif n == 1:
                # For n=1, S_1 is the trivial group.
                # If degree > 1 and f is irreducible over K, the Galois group is non-trivial.
                if d > 1:
                    factored = sympy.factor(f)
                    if not isinstance(factored, (sympy.Mul, sympy.Pow)):
                        neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: t_1, ..., t_n are algebraically independent variables over F",
    "H_3: K = F(t_1, ..., t_n) is the field of rational functions",
    "H_4: E is the splitting field of f(x) over K",
    "¬Q: The Galois group Gal(E/K) is not isomorphic to S_n"
]

N_HYP = 4
NEG_Q_INDEX = 4
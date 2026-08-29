import sympy
from sympy.ntheory import factorint, isprime
from itertools import product

# Top-level setup for potential witness expressions
x0, x1, x2, x3, x4, x5, x6, x7, x8, x9 = sympy.symbols('x0:10')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (q, n, [P_1, ..., P_k])
    where q is the order of the field, n is the number of variables,
    and P_i are sympy expressions representing the polynomials.
    """
    try:
        q, n, polys = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a finite field of order q
    try:
        h1 = False
        if isinstance(q, (int, sympy.Integer)) and q >= 2:
            f = factorint(int(q))
            if len(f) == 1:
                h1 = True
    except Exception:
        h1 = False

    # H_2: P_1, ..., P_k are polynomials in n variables over F
    try:
        h2 = False
        if isinstance(n, (int, sympy.Integer)) and n >= 1 and isinstance(polys, (list, tuple)) and len(polys) >= 1:
            n_int = int(n)
            X = sympy.symbols(f'x0:{n_int}')
            all_poly = True
            for p in polys:
                p_sym = sympy.sympify(p)
                if not p_sym.free_symbols.issubset(set(X)):
                    all_poly = False
                    break
                # Verify it is a valid polynomial
                sympy.Poly(p_sym, *X)
            if all_poly:
                h2 = True
    except Exception:
        h2 = False

    def get_num_sols():
        q_int = int(q)
        n_int = int(n)
        if not isprime(q_int):
            # For simplicity and exactness, we only evaluate over prime fields F_p
            raise NotImplementedError("Only prime q is supported for evaluation")
        if q_int**n_int > 100000:
            raise ValueError("Search space too large")
        
        X = sympy.symbols(f'x0:{n_int}')
        
        compiled_polys = []
        for p in polys:
            poly_obj = sympy.Poly(sympy.sympify(p), *X)
            compiled_polys.append(poly_obj)
            
        sols = 0
        for pt in product(range(q_int), repeat=n_int):
            is_sol = True
            for poly_obj in compiled_polys:
                val = poly_obj.eval(*pt)
                if isinstance(val, float):
                    raise ValueError("Float evaluation not allowed")
                if not sympy.sympify(val).is_integer:
                    raise ValueError("Polynomial evaluated to non-integer")
                if int(val) % q_int != 0:
                    is_sol = False
                    break
            if is_sol:
                sols += 1
        return sols

    num_sols = None
    
    # H_3: The system of equations has at least one solution in F^n
    try:
        num_sols = get_num_sols()
        h3 = num_sols >= 1
    except Exception:
        h3 = False

    # ¬Q: The system of equations has strictly less than q distinct solutions in F^n
    try:
        if num_sols is not None:
            neg_q = num_sols < int(q)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: P_1, ..., P_k are polynomials in n variables over F",
    "H_3: The system of equations has at least one solution in F^n",
    "¬Q: The system of equations has strictly less than q distinct solutions in F^n"
]

N_HYP = 3
NEG_Q_INDEX = 3
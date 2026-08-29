import itertools
from sympy.ntheory import factorint
from sympy import Poly

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (q, n, polys)
    where:
      - q is the order of the finite field (an integer prime power)
      - n is the number of variables (an integer)
      - polys is a list of SymPy expressions representing the polynomials
    """
    try:
        q, n, polys = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a finite field of order q
    try:
        if q < 2:
            h1 = False
        else:
            factors = factorint(q)
            h1 = len(factors) == 1
    except Exception:
        h1 = False
        
    # Extract variables used in the polynomials
    try:
        free_syms = set()
        for p in polys:
            if hasattr(p, 'free_symbols'):
                free_syms.update(p.free_symbols)
        vars_list = sorted(list(free_syms), key=lambda s: s.name)
    except Exception:
        vars_list = []

    # H_2: The sum of the total degrees of the polynomials is strictly less than n
    try:
        deg_sum = 0
        for p in polys:
            if p == 0:
                continue
            if vars_list:
                poly_obj = Poly(p, *vars_list)
            else:
                poly_obj = Poly(p)
            deg_sum += poly_obj.total_degree()
        h2 = deg_sum < n
    except Exception:
        h2 = False
        
    # Evaluate the system of equations over F_q^n
    try:
        if h1:
            p_prime = list(factorint(q).keys())[0]
            if p_prime != q:
                # For simplicity, we only support prime fields F_p where arithmetic is modulo p.
                # If q is a prime power but not prime, evaluating modulo q is not finite field arithmetic.
                raise NotImplementedError("Only prime q is supported for evaluation")
        
        count = 0
        for pt in itertools.product(range(q), repeat=len(vars_list)):
            subs_dict = dict(zip(vars_list, pt))
            all_zero = True
            for p in polys:
                val = p.subs(subs_dict)
                if val % q != 0:
                    all_zero = False
                    break
            if all_zero:
                count += 1
        
        # Multiply by q^(n - len(vars_list)) for any variables not explicitly in the polynomials
        total_solutions = count * (q ** (n - len(vars_list)))
        
        # H_3: The system of equations has at least one solution in F^n
        h3 = total_solutions >= 1
    except Exception:
        h3 = False
        total_solutions = 0
        
    # ¬Q: The system of equations has fewer than q distinct solutions in F^n
    try:
        neg_q = total_solutions < q
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: The sum of the total degrees of the polynomials P_1, ..., P_k is strictly less than n",
    "H_3: The system of equations has at least one solution in F^n",
    "¬Q: The system of equations has fewer than q distinct solutions in F^n"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy import Matrix, QQ, ZZ
from sympy.polys.domains import GF

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def get_test_elements(domain):
    if hasattr(domain, 'is_FiniteField') and domain.is_FiniteField:
        return [domain(i) for i in range(domain.order)]
    elif hasattr(domain, 'is_RationalField') and domain.is_RationalField:
        return [domain(0), domain(1), domain(-1), domain(2), domain(1, 2), domain(-3, 4)]
    elif hasattr(domain, 'is_RealField') and domain.is_RealField:
        return [domain(0), domain(1), domain(-1), domain(2), domain(0.5)]
    elif hasattr(domain, 'is_ComplexField') and domain.is_ComplexField:
        return [domain(0), domain(1), domain(-1), domain(2), domain(0.5), domain(1j)]
    else:
        try:
            return [domain(0), domain(1), domain(-1), domain(2)]
        except Exception:
            return [0, 1, -1, 2]

def conditions(witness):
    """
    witness: A tuple (E, F, sigmas) where E and F are SymPy field domains (e.g., QQ)
             and sigmas is a list of callable homomorphisms from E to F.
    """
    try:
        E, F, sigmas = witness
    except Exception:
        return [False, False]
        
    # H_1: E and F are fields, and sigmas are homomorphisms from E to F
    h1_ok = False
    try:
        if getattr(E, 'is_Field', False) and getattr(F, 'is_Field', False):
            if isinstance(sigmas, list) and len(sigmas) > 0:
                test_elems = get_test_elements(E)
                h1_ok = True
                for sigma in sigmas:
                    # Check if sigma maps 1 to 1
                    if sigma(E(1)) != F(1):
                        h1_ok = False
                        break
                    # Check homomorphism properties on test elements
                    for x in test_elems:
                        for y in test_elems:
                            if sigma(x + y) != sigma(x) + sigma(y):
                                h1_ok = False
                                break
                            if sigma(x * y) != sigma(x) * sigma(y):
                                h1_ok = False
                                break
                        if not h1_ok:
                            break
                    if not h1_ok:
                        break
    except Exception:
        h1_ok = False

    # neg_Q: The homomorphisms sigma_1, ..., sigma_n are linearly dependent over F
    neg_q_ok = False
    try:
        n = len(sigmas)
        test_elems = get_test_elements(E)
        rows = []
        for x in test_elems:
            row = [sigma(x) for sigma in sigmas]
            rows.append(row)
        
        M = Matrix(rows)
        
        try:
            rank = M.rank()
        except Exception:
            # Fallback if exact rank computation fails for custom domain elements
            rows_float = [[float(val) for val in row] for row in rows]
            rank = Matrix(rows_float).rank()
            
        if rank < n:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: E and F are fields and sigma_i are homomorphisms from E to F",
    "¬Q: The homomorphisms sigma_1, ..., sigma_n are linearly dependent over F"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy import symbols, Poly, Matrix, isprime
from sympy.polys.domains import GF

x, t = symbols('x t')

def conditions(witness):
    """
    Witness is expected to be a tuple: (p, P_coeffs, A_coeffs)
    where:
      - p is a prime number (so F_p is a finite field).
      - P_coeffs is a list of integers representing a monic irreducible polynomial 
        of degree n >= 1 over F_p.
      - A_coeffs is a list of integers representing an element alpha in F_p[x]/(P(x)).
    """
    try:
        p, P_coeffs, A_coeffs = witness
    except Exception:
        return [False, False, False, False]
    
    # H1: F_q is a finite field
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False
        
    # H2: F_{q^n} is an extension field of degree n over F_q
    try:
        if not h1:
            h2 = False
        else:
            if not isinstance(P_coeffs, list) or not all(isinstance(c, int) for c in P_coeffs):
                h2 = False
            else:
                domain = GF(p)
                P_poly = Poly(P_coeffs, x, domain=domain)
                n = P_poly.degree()
                h2 = bool((n >= 1) and (P_poly.LC() == 1) and P_poly.is_irreducible)
    except Exception:
        h2 = False
        
    # H3: alpha is an element of F_{q^n}
    try:
        if not h1 or not h2:
            h3 = False
        else:
            h3 = bool(isinstance(A_coeffs, list) and all(isinstance(c, int) for c in A_coeffs))
    except Exception:
        h3 = False
        
    # neg_Q: The trace Tr_{F_{q^n}/F_q}(alpha) is NOT equal to the coefficient c_{n-1}
    try:
        if not (h1 and h2 and h3):
            neg_q = False
        else:
            domain = GF(p)
            P_poly = Poly(P_coeffs, x, domain=domain)
            A_poly = Poly(A_coeffs, x, domain=domain)
            n = P_poly.degree()
            
            # Construct the matrix of the linear map L_alpha: y -> alpha * y
            # using the basis {x^{n-1}, x^{n-2}, ..., x, 1}
            M = []
            for i in range(n):
                # Basis element e_i = x^{n-1-i}
                term = Poly([1] + [0]*(n - 1 - i), x, domain=domain) * A_poly
                rem = term % P_poly
                rem_coeffs = rem.all_coeffs()
                
                # Pad with leading zeros to match the basis size n
                col = [0]*(n - len(rem_coeffs)) + [int(c) % p for c in rem_coeffs]
                M.append(col)
                
            # Trace is the sum of the diagonal elements
            trace_val = sum(M[i][i] for i in range(n)) % p
            
            # Characteristic polynomial of the matrix
            Mat = Matrix(n, n, lambda j, i: M[i][j])
            char_poly = Mat.charpoly(t)
            char_coeffs = char_poly.all_coeffs()
            
            # The coefficient c_{n-1} is the second coefficient of the characteristic polynomial
            c_n_minus_1 = int(char_coeffs[1]) % p if n >= 1 else 0
            
            neg_q = bool(trace_val != c_n_minus_1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field",
    "H_2: F_{q^n} is an extension field of degree n over F_q",
    "H_3: alpha is an element of F_{q^n}",
    "¬Q: The trace Tr_{F_{q^n}/F_q}(alpha) is NOT equal to the coefficient c_{n-1}"
]

N_HYP = 3
NEG_Q_INDEX = 3
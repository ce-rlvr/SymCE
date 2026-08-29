import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: E/F is a finite field extension",
    "¬Q: The field trace Tr_{E/F}(alpha) is not equal to -degree(E/F(alpha)) a_{d-1}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        x = sp.Symbol('x')
        
        # Case 1: witness is a matrix representing multiplication by alpha in E/F
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            M = witness
            n = M.shape[0]
            charpoly = M.charpoly(x)
            factors = sp.factor_list(charpoly.as_expr())
            
            if len(factors[1]) == 1:
                minpoly_expr = factors[1][0][0]
                minpoly = sp.Poly(minpoly_expr, x)
                h1 = minpoly.is_irreducible
                
                trace_alpha = M.trace()
                minpoly = minpoly.monic()
                d = minpoly.degree()
                coeffs = minpoly.all_coeffs()
                a_d_minus_1 = coeffs[1] if len(coeffs) > 1 else 0
                m = n // d
                expected = -m * a_d_minus_1
                
                neg_q = (trace_alpha != expected)
                return [bool(h1), bool(neg_q)]
            else:
                return [False, False]
                
        # Case 2: witness is a tuple (P, A) where P is the irreducible polynomial defining E/F
        # and A is the polynomial representing alpha
        elif isinstance(witness, tuple) and len(witness) == 2:
            P_expr, A_expr = witness
            P = sp.Poly(P_expr, x)
            A = sp.Poly(A_expr, x)
            
            h1 = P.is_irreducible
            if not h1:
                return [False, False]
                
            n = P.degree()
            if n < 1:
                return [False, False]
                
            M = sp.zeros(n, n)
            for j in range(n):
                rem = sp.rem(A * sp.Poly(x**j, x, domain=P.domain), P)
                coeffs = rem.all_coeffs()
                coeffs = [0]*(n - len(coeffs)) + coeffs
                for i in range(n):
                    M[n-1-i, j] = coeffs[i]
                    
            trace_alpha = M.trace()
            charpoly = M.charpoly(x)
            factors = sp.factor_list(charpoly.as_expr())
            
            if len(factors[1]) == 1:
                minpoly_expr = factors[1][0][0]
            else:
                minpoly_expr = charpoly.as_expr()
                
            minpoly = sp.Poly(minpoly_expr, x, domain=P.domain)
            minpoly = minpoly.monic()
            d = minpoly.degree()
            coeffs = minpoly.all_coeffs()
            a_d_minus_1 = coeffs[1] if len(coeffs) > 1 else 0
            m = n // d
            expected = -m * a_d_minus_1
            
            neg_q = (trace_alpha != expected)
            return [bool(h1), bool(neg_q)]
            
        # Case 3: witness is a tuple (minpoly_coeffs, m, trace_val)
        elif isinstance(witness, tuple) and len(witness) == 3:
            coeffs, m, trace_val = witness
            if isinstance(coeffs, list) and len(coeffs) > 0:
                a_d_minus_1 = coeffs[1] if len(coeffs) > 1 else 0
                expected = -m * a_d_minus_1
                neg_q = (trace_val != expected)
                return [True, bool(neg_q)]
                
    except Exception:
        pass
        
    return [False, False]
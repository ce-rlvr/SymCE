import sympy
from sympy import symbols, groebner, reduced
import sympy.combinatorics
import sympy.matrices

# Top-level setup for standard algebra objects
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f(x) is nilpotent in the formal power series ring",
    "¬Q: There exists i >= 0 such that a_i is not nilpotent in R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Evaluates the conditions for the conjecture.
    The witness is expected to be a dictionary defining the ring and the power series.
    
    Format for Z/nZ:
    {
        'ring_type': 'Z/nZ',
        'n': 8,
        'coeffs': [2, 4, 0, ...], # coefficients a_0, a_1, ...
        'N': 3,              # nilpotency index of f(x)
        'check_degree': 5,   # degree up to which f(x)^N = 0 is checked
        'target_i': 1        # index of the coefficient claimed to be non-nilpotent
    }
    
    Format for polynomial quotient ring Q[vars]/ideal:
    {
        'ring_type': 'poly_quotient',
        'vars': ['x', 'y'],
        'ideal': ['x**2', 'y**2'],
        'coeffs': ['x', 'y', ...],
        'N': 2,
        'check_degree': 3,
        'target_i': 1
    }
    """
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        ring_type = witness.get('ring_type')
        
        if ring_type == 'Z/nZ':
            n = int(witness['n'])
            coeffs = [int(c) for c in witness['coeffs']]
            N = min(int(witness['N']), 100)
            check_degree = min(int(witness.get('check_degree', len(coeffs))), 100)
            target_i = int(witness['target_i'])
            
            if N <= 0 or n <= 1 or target_i >= len(coeffs):
                return [False, False, False]
                
            h1 = True # Z/nZ is always commutative
            
            def multiply_series(A, B, deg):
                C = [0] * (deg + 1)
                for i in range(min(len(A), deg + 1)):
                    if A[i] == 0: continue
                    for j in range(min(len(B), deg + 1 - i)):
                        if B[j] == 0: continue
                        C[i+j] = (C[i+j] + A[i] * B[j]) % n
                return C
                
            res = [1] + [0] * check_degree
            base = [c % n for c in coeffs]
            
            exp = N
            while exp > 0:
                if exp % 2 == 1:
                    res = multiply_series(res, base, check_degree)
                base = multiply_series(base, base, check_degree)
                exp //= 2
                
            h2 = all(c == 0 for c in res)
                
            a_i = coeffs[target_i] % n
            neg_q = (pow(a_i, n, n) != 0)
                
            return [h1, h2, neg_q]
            
        elif ring_type == 'poly_quotient':
            vars_list = witness['vars']
            var_symbols = [sympy.Symbol(v) for v in vars_list]
            local_dict = {v: sympy.Symbol(v) for v in vars_list}
            
            ideal = [sympy.sympify(p, locals=local_dict) for p in witness['ideal']]
            coeffs = [sympy.sympify(c, locals=local_dict) for c in witness['coeffs']]
            N = min(int(witness['N']), 50)
            check_degree = min(int(witness.get('check_degree', len(coeffs))), 50)
            target_i = int(witness['target_i'])
            
            if N <= 0 or target_i >= len(coeffs):
                return [False, False, False]
                
            h1 = True # Polynomial quotient rings are commutative
            
            gb = sympy.groebner(ideal, *var_symbols) if ideal else None
            
            def multiply_series_poly(A, B, deg):
                C = [sympy.S.Zero] * (deg + 1)
                for i in range(min(len(A), deg + 1)):
                    if A[i] == 0: continue
                    for j in range(min(len(B), deg + 1 - i)):
                        if B[j] == 0: continue
                        C[i+j] = C[i+j] + A[i] * B[j]
                
                if gb is not None:
                    for k in range(deg + 1):
                        if C[k] != 0:
                            C[k] = sympy.reduced(C[k], gb, var_symbols)[1]
                else:
                    for k in range(deg + 1):
                        if C[k] != 0:
                            C[k] = sympy.expand(C[k])
                return C

            res = [sympy.S.One] + [sympy.S.Zero] * check_degree
            base = list(coeffs)
            
            exp = N
            while exp > 0:
                if exp % 2 == 1:
                    res = multiply_series_poly(res, base, check_degree)
                base = multiply_series_poly(base, base, check_degree)
                exp //= 2
                
            h2 = all(sympy.expand(c) == 0 for c in res)
                
            a_i = coeffs[target_i]
            if ideal:
                y = sympy.Symbol('y_rabinowitsch')
                rabinowitsch_ideal = ideal + [1 - y * a_i]
                gb_rab = sympy.groebner(rabinowitsch_ideal, *(var_symbols + [y]))
                is_unit_ideal = any(sympy.expand(g) == 1 for g in gb_rab)
                neg_q = not is_unit_ideal
            else:
                neg_q = (sympy.expand(a_i) != 0)
                
            return [h1, h2, neg_q]
            
    except Exception:
        pass

    return [False, False, False]
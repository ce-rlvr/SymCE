import sympy
import sympy.combinatorics
import sympy.matrices
import z3
from sympy.abc import x

# Top-level setup
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

def is_nilpotent_zn_elem(a, n):
    if n == 1: return True
    if n == 0: return a == 0
    factors = sympy.factorint(n)
    for p in factors:
        if a % p != 0:
            return False
    return True

def is_unit_zn(A, n):
    A_poly = sympy.Poly(A, x)
    coeffs = A_poly.all_coeffs()
    if not coeffs:
        return False
    if n == 0:
        return A_poly.degree() == 0 and coeffs[0] in [1, -1]
        
    a0 = coeffs[-1]
    if sympy.gcd(a0, n) != 1:
        return False
    for a in coeffs[:-1]:
        if not is_nilpotent_zn_elem(a, n):
            return False
    return True

def is_irreducible_zn(P, n):
    if is_unit_zn(P, n):
        return False
    P_poly = sympy.Poly(P, x)
    P_deg = P_poly.degree()
    if P_deg < 0:
        return False
        
    if n == 0:
        try:
            factors = sympy.factor_list(P_poly)
            if len(factors[1]) == 0:
                return sympy.isprime(abs(factors[0]))
            if len(factors[1]) == 1 and factors[1][0][1] == 1:
                return abs(factors[0]) == 1
            return False
        except Exception:
            return False

    max_deg = max(1, P_deg + 1)
    
    solver = z3.Solver()
    A_coeffs = [z3.Int(f'a_{i}') for i in range(max_deg + 1)]
    B_coeffs = [z3.Int(f'b_{i}') for i in range(max_deg + 1)]
    
    P_c = [int(P_poly.nth(i)) for i in range(P_deg + 1)]
    for k in range(2 * max_deg + 1):
        c_k = sum(A_coeffs[i] * B_coeffs[k - i] for i in range(max_deg + 1) if 0 <= k - i <= max_deg)
        p_k = P_c[k] if k <= P_deg else 0
        solver.add((c_k - p_k) % n == 0)
        
    def z3_is_unit(coeffs):
        units_zn = [i for i in range(n) if sympy.gcd(i, n) == 1]
        cond_a0 = z3.Or([coeffs[0] % n == u for u in units_zn])
        
        nilpotents_zn = [i for i in range(n) if is_nilpotent_zn_elem(i, n)]
        if len(coeffs) > 1:
            cond_ai = z3.And([z3.Or([coeffs[i] % n == nilp for nilp in nilpotents_zn]) for i in range(1, len(coeffs))])
            return z3.And(cond_a0, cond_ai)
        else:
            return cond_a0
            
    solver.add(z3.Not(z3_is_unit(A_coeffs)))
    solver.add(z3.Not(z3_is_unit(B_coeffs)))
    
    return solver.check() == z3.unsat

def check_divides_zn(A, B, n):
    A_poly = sympy.Poly(A, x)
    B_poly = sympy.Poly(B, x)
    
    if n == 0:
        try:
            q, r = sympy.div(B_poly, A_poly)
            return r.is_zero
        except Exception:
            return False
            
    A_deg = A_poly.degree()
    B_deg = B_poly.degree()
    if A_deg < 0:
        return B_deg < 0
    if B_deg < 0:
        return True
        
    max_deg = max(A_deg, B_deg) + 3
    
    solver = z3.Solver()
    Q_coeffs = [z3.Int(f'q_{i}') for i in range(max_deg + 1)]
    
    A_c = [int(A_poly.nth(i)) for i in range(A_deg + 1)]
    B_c = [int(B_poly.nth(i)) for i in range(B_deg + 1)]
    
    for k in range(A_deg + max_deg + 1):
        c_k = sum(A_c[i] * Q_coeffs[k - i] for i in range(A_deg + 1) if 0 <= k - i <= max_deg)
        b_k = B_c[k] if k <= B_deg else 0
        solver.add((c_k - b_k) % n == 0)
        
    return solver.check() == z3.sat

def check_nilpotent_zn(f, p, n, max_m=6):
    for m in range(1, max_m + 1):
        if check_divides_zn(p, f**m, n):
            return True
    return False

def conditions(witness):
    try:
        if len(witness) == 4:
            n_obj, p, factors, f = witness
            if isinstance(n_obj, int):
                n = n_obj
            elif hasattr(n_obj, 'mod'):
                n = int(n_obj.mod)
            elif hasattr(n_obj, 'order'):
                n = int(n_obj.order)
            else:
                try:
                    n = int(n_obj)
                except Exception:
                    return [False, False, False, False]
        else:
            return [False, False, False, False]
            
        if n < 0 or n == 1:
            return [False, False, False, False]
            
        # H1: p is non-constant
        try:
            p_poly = sympy.Poly(p, x)
            deg = p_poly.degree()
            h1 = False if deg < 0 else int(deg) >= 1
        except Exception:
            h1 = False
            
        # H2: factors are distinct and irreducible, and p divides their product^m
        try:
            h2 = True
            if not factors:
                h2 = False
            else:
                for fac in factors:
                    if not is_irreducible_zn(fac, n):
                        h2 = False
                        break
                    if not check_divides_zn(fac, p, n):
                        h2 = False
                        break
                
                if h2:
                    for i in range(len(factors)):
                        for j in range(i + 1, len(factors)):
                            if check_divides_zn(factors[i], factors[j], n) and check_divides_zn(factors[j], factors[i], n):
                                h2 = False
                                break
                                
                if h2:
                    prod = 1
                    for fac in factors:
                        prod = prod * fac
                    
                    missing_factors = True
                    for m in range(1, 6):
                        if check_divides_zn(p, prod**m, n):
                            missing_factors = False
                            break
                    if missing_factors:
                        h2 = False
        except Exception:
            h2 = False
            
        # H3: f is a polynomial
        try:
            f_poly = sympy.Poly(f, x)
            h3 = True
        except Exception:
            h3 = False
            
        # Neg Q:
        try:
            prod = 1
            for fac in factors:
                prod = prod * fac
                
            is_nilp = check_nilpotent_zn(f, p, n)
            divides = check_divides_zn(prod, f, n)
            
            neg_q = is_nilp != divides
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: p(x) is a non-constant polynomial",
    "H_2: p_1(x), ..., p_k(x) are the distinct irreducible factors of p(x)",
    "H_3: f(x) is a polynomial",
    "¬Q: f(x) + (p(x)) is nilpotent XOR product of p_i(x) divides f(x)"
]
N_HYP = 3
NEG_Q_INDEX = 3
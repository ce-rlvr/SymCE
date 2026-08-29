import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, eye, zeros, Symbol, Poly, rem, simplify
import itertools

# Top-level setup for standard named objects
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (A, lam, k) for standard matrices over fields,
    or (A, lam, k, modulus) for matrices over the ring Z/nZ.
    """
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                A, lam, k, n = witness
                is_ring = True
            elif len(witness) == 3:
                A, lam, k = witness
                is_ring = False
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    if is_ring:
        try:
            rows, cols = A.shape
            if rows != cols or rows == 0:
                return [False, False, False]
                
            is_eigenvalue = False
            null_vectors = []
            for v_tup in itertools.product(range(n), repeat=cols):
                v = Matrix(cols, 1, v_tup)
                Av = A * v
                lam_v = lam * v
                if all((Av[i] - lam_v[i]) % n == 0 for i in range(cols)):
                    null_vectors.append(v_tup)
                    if any(val != 0 for val in v_tup):
                        is_eigenvalue = True
                        
            h1 = is_eigenvalue
            
            x = Symbol('x')
            cp = A.charpoly(x)
            cp_coeffs = [c % n for c in cp.all_coeffs()]
            
            def divides_mod_n(coeffs_dividend, m):
                if m == 0:
                    return True
                div_expr = ((x - lam)**m).expand()
                div_poly = Poly(div_expr, x)
                div_coeffs = [c % n for c in div_poly.all_coeffs()]
                
                rem_list = list(coeffs_dividend)
                while len(rem_list) >= len(div_coeffs):
                    if rem_list[0] % n == 0:
                        rem_list.pop(0)
                        continue
                    factor = rem_list[0]
                    for i in range(len(div_coeffs)):
                        rem_list[i] = (rem_list[i] - factor * div_coeffs[i]) % n
                    rem_list.pop(0)
                return all(c % n == 0 for c in rem_list)
                
            actual_k = 0
            for m in range(1, cols + 1):
                if divides_mod_n(cp_coeffs, m):
                    actual_k = m
                else:
                    break
                    
            h2 = (k == actual_k)
            
            dim = 0
            if len(null_vectors) > 1:
                found = False
                for d in range(1, cols + 1):
                    for gens in itertools.combinations(null_vectors, d):
                        generated = set()
                        for coeffs in itertools.product(range(n), repeat=d):
                            vec = tuple(sum(coeffs[i] * gens[i][j] for i in range(d)) % n for j in range(cols))
                            generated.add(vec)
                        if len(generated) == len(null_vectors):
                            dim = d
                            found = True
                            break
                    if found:
                        break
                        
            neg_q = dim > k
            
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            return [False, False, False]
    else:
        try:
            rows, cols = A.shape
            if rows != cols or rows == 0:
                return [False, False, False]
            
            M = A - lam * eye(rows)
            ns = M.nullspace()
            
            h1 = len(ns) > 0
            
            x = Symbol('x')
            cp = A.charpoly(x).as_expr()
            actual_k = 0
            for m in range(1, cols + 1):
                rem_expr = rem(cp, (x - lam)**m, x)
                if rem_expr == 0 or simplify(rem_expr) == 0:
                    actual_k = m
                else:
                    break
                    
            h2 = (k == actual_k)
            
            dim = len(ns)
            neg_q = dim > k
            
            return [bool(h1), bool(h2), bool(neg_q)]
        except Exception:
            return [False, False, False]

CONDITION_LABELS = [
    "H_1: Let lambda be an eigenvalue of A",
    "H_2: Let k be the algebraic multiplicity of lambda as a root of the characteristic polynomial of A",
    "¬Q: The dimension of the null space of A - lambda I is strictly greater than k"
]

N_HYP = 2
NEG_Q_INDEX = 2
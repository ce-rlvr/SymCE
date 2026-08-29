import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x
import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def is_irreducible(M, n):
    if n == 1:
        return True
    
    basis = [eye(n)]
    while True:
        new_basis = list(basis)
        for m in M:
            for b in basis:
                mb = m * b
                vecs = [list(mat) for mat in new_basis]
                vecs.append(list(mb))
                if Matrix(vecs).rank() > len(new_basis):
                    new_basis.append(mb)
        if len(new_basis) == len(basis):
            break
        basis = new_basis
        
    dimA = len(basis)
    if dimA == n * n:
        return True
        
    if dimA == n:
        for coeffs in itertools.product([-1, 0, 1], repeat=dimA):
            if all(c == 0 for c in coeffs): 
                continue
            mat = sum((c * b for c, b in zip(coeffs, basis)), zeros(n, n))
            cp_expr = mat.charpoly(x).as_expr()
            if sympy.Poly(cp_expr, x, domain='QQ').is_irreducible:
                return True
        return False
        
    return False

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 2:
            return [False, False, False, False]
        M, phi = witness
        
        if not isinstance(M, list):
            return [False, False, False, False]
        if not isinstance(phi, Matrix):
            return [False, False, False, False]
            
        if not phi.is_square:
            return [False, False, False, False]
            
        n = phi.shape[0]
        if n < 1:
            return [False, False, False, False]
            
        rational_entries = True
        for m in M:
            if not isinstance(m, Matrix) or m.shape != (n, n):
                rational_entries = False
                break
            for val in list(m):
                if not val.is_Rational:
                    rational_entries = False
                    break
        if not rational_entries:
            return [False, False, False, False]
            
        for val in list(phi):
            if not val.is_Rational:
                rational_entries = False
                break
                
        if not rational_entries:
            return [False, False, False, False]
            
        # H_1: G is a group (M generates a group, so we check if all generators are invertible)
        h1 = True
        for m in M:
            if m.det() == 0:
                h1 = False
                break
                
        # H_2: V is a finite-dimensional irreducible representation of G over K
        h2 = False
        if h1:
            h2 = is_irreducible(M, n)
            
        # H_3: phi is a G-equivariant K-linear map from V to V
        h3 = True
        for m in M:
            if m * phi != phi * m:
                h3 = False
                break
                
        # ¬Q: phi is not a scalar multiple of the identity map
        neg_q = True
        if n > 0:
            c = phi[0, 0]
            if phi == c * eye(n):
                neg_q = False
                
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: V is a finite-dimensional irreducible representation of G over K",
    "H_3: phi is a G-equivariant K-linear map from V to V",
    "¬Q: phi is not a scalar multiple of the identity map"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_isomorphism(G, A):
    """
    Checks if matrix A represents an isomorphism on the finitely generated 
    abelian group G = Z/m_1 Z x ... x Z/m_n Z.
    G is given as a list of moduli (0 means Z).
    """
    try:
        if not isinstance(A, sympy.Matrix):
            try:
                A = sympy.Matrix(A)
            except Exception:
                return False
                
        n = len(G)
        if A.shape != (n, n): 
            return False
        
        # Check if A is a well-defined homomorphism
        for j in range(n):
            for i in range(n):
                try:
                    val = int(A[i, j])
                    if val != A[i, j]: 
                        return False
                except Exception:
                    return False
                    
                if G[j] != 0:
                    if G[i] == 0:
                        if val != 0: 
                            return False
                    else:
                        if (G[j] * val) % G[i] != 0: 
                            return False

        # Check if A is an isomorphism by finding an inverse homomorphism B
        solver = z3.Solver()
        B = [[z3.Int(f'B_{i}_{j}') for j in range(n)] for i in range(n)]
        
        # B must be well-defined
        for j in range(n):
            for i in range(n):
                if G[j] != 0:
                    if G[i] == 0:
                        solver.add(B[i][j] == 0)
                    else:
                        k = z3.Int(f'k_{i}_{j}')
                        solver.add(B[i][j] * G[j] == k * G[i])
                        
        # A * B = I mod M and B * A = I mod M
        for i in range(n):
            for j in range(n):
                dot1 = sum(int(A[i, k]) * B[k][j] for k in range(n))
                if i == j:
                    if G[i] == 0:
                        solver.add(dot1 == 1)
                    else:
                        c = z3.Int(f'c1_{i}_{j}')
                        solver.add(dot1 == 1 + c * G[i])
                else:
                    if G[i] == 0:
                        solver.add(dot1 == 0)
                    else:
                        c = z3.Int(f'c1_{i}_{j}')
                        solver.add(dot1 == c * G[i])
                        
                dot2 = sum(B[i][k] * int(A[k, j]) for k in range(n))
                if i == j:
                    if G[i] == 0:
                        solver.add(dot2 == 1)
                    else:
                        c = z3.Int(f'c2_{i}_{j}')
                        solver.add(dot2 == 1 + c * G[i])
                else:
                    if G[i] == 0:
                        solver.add(dot2 == 0)
                    else:
                        c = z3.Int(f'c2_{i}_{j}')
                        solver.add(dot2 == c * G[i])
                        
        return solver.check() == z3.sat
    except Exception:
        return False

def is_isomorphism_hom(phi):
    try:
        return phi.is_injective() and phi.is_surjective()
    except Exception:
        return False

def conditions(witness):
    """
    Evaluates the remaining hypotheses and the negated conclusion.
    The witness can be:
      - A sympy Homomorphism object
      - A tuple (G, phi) where G is a sympy group and phi is a Homomorphism
      - A tuple (G, A) where G is a list of moduli (e.g. [0, 2] for Z x Z_2) and A is a matrix
      - A sympy Matrix A (implicitly assuming G = Z^n)
    """
    try:
        # Case 1: witness is a Homomorphism
        if hasattr(witness, 'domain') and hasattr(witness, 'is_injective'):
            G = witness.domain
            h1_ok = getattr(G, 'is_abelian', False)
            iso = is_isomorphism_hom(witness)
            return [bool(h1_ok), not iso]
            
        # Case 2: witness is a tuple (G, phi)
        if isinstance(witness, tuple) and len(witness) == 2:
            G, phi = witness
            
            # Subcase 2a: phi is a Homomorphism
            if hasattr(phi, 'domain') and hasattr(phi, 'is_injective'):
                h1_ok = getattr(G, 'is_abelian', False)
                iso = is_isomorphism_hom(phi)
                return [bool(h1_ok), not iso]
                
            # Subcase 2b: G is a list/tuple of ints, phi is a Matrix
            if isinstance(G, (list, tuple)) and all(isinstance(x, int) and x >= 0 for x in G):
                h1_ok = True
                iso = is_isomorphism(list(G), phi)
                return [h1_ok, not iso]
                
        # Case 3: witness is just a Matrix (assume G = Z^n)
        if isinstance(witness, sympy.Matrix) or (isinstance(witness, list) and all(isinstance(row, list) for row in witness)):
            A = sympy.Matrix(witness)
            G = [0] * A.shape[0]
            h1_ok = True
            iso = is_isomorphism(G, A)
            return [h1_ok, not iso]
            
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: G is a finitely generated abelian group",
    "¬Q: phi is not an isomorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1
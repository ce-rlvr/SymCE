import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import Matrix, eye, zeros
import math

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses
    and if it falsifies the conclusion of the Hyperplane Kernel Theorem.
    
    The witness can be:
      - A tuple (f, m) where f is a 1 x n SymPy Matrix and m is an integer modulus.
      - A 1 x n SymPy Matrix of sympy.Mod objects.
      - A standard 1 x n SymPy Matrix (evaluated over a field).
    """
    try:
        # Case 1: Witness is a tuple of (Matrix, modulus) representing a module over Z_m
        if isinstance(witness, tuple) and len(witness) == 2:
            f, m = witness
            if not hasattr(f, 'shape') or f.shape[0] != 1:
                return [False, False]
            
            f_vals = [int(x) % m for x in f]
            
            # H1: f is a non-zero linear functional
            H1 = any(x != 0 for x in f_vals)
            
            # Compute the image size to find the quotient size
            g = m
            for x in f_vals:
                g = math.gcd(g, x)
                
            quotient_size = m // g
            
            # neg_Q: The kernel does not have codimension 1
            # (Codimension 1 implies the quotient size is exactly m)
            neg_Q = quotient_size != m
            return [H1, neg_Q]
            
        # Case 2 & 3: Witness is a SymPy Matrix
        elif hasattr(witness, 'shape'):
            f = witness
            if f.shape[0] != 1:
                return [False, False]
                
            # Case 2: Matrix of Mod objects
            if any(isinstance(x, sympy.Mod) for x in f):
                m = int(f[0].args[1])
                f_vals = [int(x.args[0]) % m for x in f]
                
                H1 = any(x != 0 for x in f_vals)
                
                g = m
                for x in f_vals:
                    g = math.gcd(g, x)
                    
                quotient_size = m // g
                neg_Q = quotient_size != m
                return [H1, neg_Q]
                
            # Case 3: Standard Matrix over a field
            else:
                H1 = not f.is_zero_matrix
                
                # Over a field, codimension is dimension of V minus dimension of kernel
                codim = f.shape[1] - len(f.nullspace())
                neg_Q = codim != 1
                return [H1, neg_Q]
                
    except Exception:
        pass
        
    return [False, False]

CONDITION_LABELS = [
    "H_1: f is a non-zero linear functional in V^*",
    "¬Q: The kernel of f is not a subspace of V of codimension 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
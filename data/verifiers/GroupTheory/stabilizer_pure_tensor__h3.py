import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary with keys 'G_V', 'G_W', 'v', 'w',
    or a tuple (G_V, G_W, v, w).
    G_V and G_W are lists of matrices representing the generators (or full group) 
    of the action on V and W respectively.
    v and w are the vectors (as lists or sympy Matrices).
    """
    try:
        if isinstance(witness, dict):
            G_V = witness.get('G_V', [])
            G_W = witness.get('G_W', [])
            v = witness.get('v', None)
            w = witness.get('w', None)
        else:
            G_V, G_W, v, w = witness
            
        if not G_V or not G_W or len(G_V) != len(G_W) or v is None or w is None:
            return [False, False, False]
            
        G_V = [Matrix(g) if not isinstance(g, Matrix) else g for g in G_V]
        G_W = [Matrix(g) if not isinstance(g, Matrix) else g for g in G_W]
        v = Matrix(v) if not isinstance(v, Matrix) else v
        w = Matrix(w) if not isinstance(w, Matrix) else w
        
        # Compute closure to ensure the provided matrices generate a finite group
        pairs = list(zip(G_V, G_W))
        closure = []
        for p in pairs:
            if p not in closure:
                closure.append(p)
        
        head = 0
        while head < len(closure):
            a = closure[head]
            for b in pairs:
                prod = (a[0] * b[0], a[1] * b[1])
                if prod not in closure:
                    closure.append(prod)
                    if len(closure) > 200:
                        # Group too large or infinite
                        return [False, False, False]
            head += 1
            
        n_V = G_V[0].shape[0]
        n_W = G_W[0].shape[0]
        id_V = eye(n_V)
        id_W = eye(n_W)
        
        # H1: G is a group acting linearly on vector spaces V and W
        if (id_V, id_W) not in closure:
            return [False, False, False]
        h1 = True
        
        # H2: G acts on the tensor product V ⊗ W via g · (v ⊗ w) = (g · v) ⊗ (g · w)
        # This is true by definition of the tensor product representation.
        h2 = True
        
        def kron(A, B):
            rA, cA = A.shape
            rB, cB = B.shape
            return Matrix(rA * rB, cA * cB, lambda i, j: A[i // rB, j // cB] * B[i % rB, j % cB])
            
        vw = kron(v, w)
        stab_int = set()
        stab_tens = set()
        
        for i, (gv, gw) in enumerate(closure):
            if gv * v == v and gw * w == w:
                stab_int.add(i)
            if kron(gv, gw) * vw == vw:
                stab_tens.add(i)
                
        # The literal conjecture claims Stab_G(v) ∩ Stab_G(w) is a subgroup of Stab_G(v ⊗ w),
        # which is a tautology. The intended false conjecture (and its negation) concerns 
        # whether they are equal or if the reverse inclusion holds.
        # neg_Q is True if Stab_G(v ⊗ w) contains elements not in Stab_G(v) ∩ Stab_G(w).
        neg_q = not stab_tens.issubset(stab_int)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting linearly on vector spaces V and W over the same field",
    "H_2: G acts on the tensor product V ⊗ W via g · (v ⊗ w) = (g · v) ⊗ (g · w)",
    "¬Q: The point stabilizer Stab_G(v ⊗ w) is strictly larger than the intersection Stab_G(v) ∩ Stab_G(w)"
]

N_HYP = 2
NEG_Q_INDEX = 2
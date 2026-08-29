import sympy
from sympy import Matrix, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
import math
from sympy.ntheory import factorint
from sympy.matrices.normalforms import smith_normal_form

# Top-level setup: named object bindings that the witness expression may reference.
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

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "A finitely generated module over a commutative local ring is free."
    
    The witness should be a tuple (R, M) where:
      - R is represented by an integer n >= 2, corresponding to the ring Z/nZ.
        (Z/nZ is a local ring iff n = p^k for some prime p).
      - M is the module, which can be represented as:
          * A list of integers [d_1, ..., d_k] representing Z/d_1 Z ⊕ ... ⊕ Z/d_k Z.
          * A SymPy AbelianGroup or CyclicGroup.
          * A SymPy Matrix representing a presentation matrix over Z/nZ.
          * A single integer d representing Z/d Z.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        
        n, M = witness
        
        # Extract n (the ring Z/nZ)
        if hasattr(n, 'is_cyclic') and callable(getattr(n, 'order', None)):
            if n.is_cyclic:
                n = int(n.order())
                
        if not isinstance(n, (int, sympy.Integer)):
            return [False, False, False]
            
        n = int(n)
        if n < 2:
            return [False, False, False]
            
        # Extract the invariant factors of the module M
        d_list = None
        if isinstance(M, (int, sympy.Integer)):
            d_list = [int(M)]
        elif isinstance(M, (list, tuple)):
            d_list = []
            for d in M:
                if hasattr(d, 'is_cyclic') and callable(getattr(d, 'order', None)) and d.is_cyclic:
                    d_list.append(int(d.order()))
                elif isinstance(d, (int, sympy.Integer)):
                    d_list.append(int(d))
                else:
                    return [False, False, False]
        elif hasattr(M, 'is_abelian') and callable(getattr(M, 'abelian_invariants', None)):
            if not M.is_abelian:
                return [False, False, False]
            d_list = [int(d) for d in M.abelian_invariants()]
        elif isinstance(M, Matrix):
            snf = smith_normal_form(M)
            r, c = M.shape
            d_list = [math.gcd(int(snf[i, i]), n) for i in range(min(r, c))]
            d_list += [n] * (r - min(r, c))
            
        if d_list is None:
            return [False, False, False]
            
        for d in d_list:
            if not isinstance(d, (int, sympy.Integer)) or d < 1:
                return [False, False, False]
                
        # H_1: R is a commutative local ring
        # Z/nZ is a local ring if and only if n is a prime power.
        factors = factorint(n)
        h1 = (len(factors) == 1)
        
        # H_2: M is a finitely generated module over R
        # M is a module over Z/nZ if and only if n annihilates M (i.e., d_i divides n for all i).
        h2 = all(n % d == 0 for d in d_list)
        
        # ¬Q: M is NOT a free R-module
        # M is free over Z/nZ if and only if it is isomorphic to (Z/nZ)^k.
        # This means all non-trivial invariant factors must be exactly n.
        is_free = all(d == n for d in d_list if d > 1)
        neg_q = not is_free
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "H_2: M is a finitely generated module over R",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
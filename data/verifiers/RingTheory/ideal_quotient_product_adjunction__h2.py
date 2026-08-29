import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup for potential witness expressions
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "In a commutative ring R, for any subsets I, J, K, I \subseteq (K : J) iff IJ \subseteq K."
    
    The witness can be provided in two formats:
      1. (n, I, J, K) where n is an integer >= 2 representing the ring Z_n, 
         and I, J, K are iterables of integers in Z_n.
      2. (I, J, K) where I, J, K are iterables of integers, evaluated in the ring Z.
    """
    try:
        if len(witness) == 4:
            n, I, J, K = witness
            n = int(n)
            if n < 2:
                return [False, False]
            
            I = set(int(x) for x in I)
            J = set(int(x) for x in J)
            K = set(int(x) for x in K)
            
            if not all(0 <= x < n for x in I | J | K):
                return [False, False]
                
            # H_1: R is a commutative ring (Z_n is always a commutative ring)
            h1 = True
            
            # Compute the ideal quotient (K : J) = {r \in R | rJ \subseteq K}
            K_colon_J = set()
            for r in range(n):
                if all((r * j) % n in K for j in J):
                    K_colon_J.add(r)
                    
            I_sub_K_colon_J = I.issubset(K_colon_J)
            
            # Compute the product IJ (additive closure of {i*j | i \in I, j \in J})
            products = set((i * j) % n for i in I for j in J)
            IJ = {0} | products
            queue = list(IJ)
            while queue:
                x = queue.pop(0)
                for y in list(IJ):
                    z = (x + y) % n
                    if z not in IJ:
                        IJ.add(z)
                        queue.append(z)
                        
            IJ_sub_K = IJ.issubset(K)
            
            # ¬Q: The equivalence fails
            neg_q = (I_sub_K_colon_J != IJ_sub_K)
            return [h1, neg_q]
            
        elif len(witness) == 3:
            I, J, K = witness
            I = set(int(x) for x in I)
            J = set(int(x) for x in J)
            K = set(int(x) for x in K)
            
            # H_1: R is a commutative ring (Z is a commutative ring)
            h1 = True
            
            # I \subseteq (K : J)
            I_sub_K_colon_J = all(all(i * j in K for j in J) for i in I)
            
            # IJ \subseteq K
            # In Z, the additive closure of any non-zero element is infinite.
            # Since K is a finite set, IJ \subseteq K is only possible if products == {0} or empty.
            products = set(i * j for i in I for j in J)
            if not products or products == {0}:
                IJ_sub_K = (0 in K)
            else:
                IJ_sub_K = False
                
            # ¬Q: The equivalence fails
            neg_q = (I_sub_K_colon_J != IJ_sub_K)
            return [h1, neg_q]
            
        else:
            return [False, False]
            
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: Equivalence I \\subseteq (K : J) iff IJ \\subseteq K fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
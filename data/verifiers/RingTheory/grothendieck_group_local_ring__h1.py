import sympy
from sympy import ZZ, QQ
from sympy.ntheory import factorint

N_HYP = 0
NEG_Q_INDEX = 0
CONDITION_LABELS = ["¬Q: K_0(R) is not isomorphic to Z"]

def conditions(witness):
    try:
        def get_k0_rank(w):
            # Base rings with K_0(R) == Z
            if w in (ZZ, QQ, sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes):
                return 1
            
            # Finite fields have K_0(R) == Z
            if type(w).__name__ in ('FiniteField', 'GMPYFiniteField', 'PythonFiniteField'):
                return 1
                
            # Polynomial rings have the same K_0 as their base ring
            if hasattr(w, 'domain') and hasattr(w, 'gens'):
                return get_k0_rank(w.domain)
                
            # Integers n represent the ring Z/nZ
            if isinstance(w, (int, sympy.Integer)):
                n = int(w)
                if n == 0:
                    return 1  # Z/0Z == Z, K_0 is Z
                elif n == 1 or n == -1:
                    return 0  # Z/1Z == 0, K_0 is 0
                else:
                    # For Z/nZ, K_0 is Z^k where k is the number of distinct prime factors
                    return len(factorint(abs(n)))
                    
            # Tuples/lists represent a product of rings
            if isinstance(w, (list, tuple, set)):
                return sum(get_k0_rank(x) for x in w)
                
            raise ValueError("Unknown ring representation")
            
        rank = get_k0_rank(witness)
        # If the rank of the free part of K_0 is not 1, it cannot be isomorphic to Z.
        # (This correctly identifies product rings and Z/nZ for composite n with >1 prime factors).
        neg_q = bool(rank != 1)
        
    except Exception:
        neg_q = False
        
    return [neg_q]
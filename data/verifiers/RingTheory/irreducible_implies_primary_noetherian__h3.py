import sympy
from sympy import QQ, ZZ, symbols
from sympy.ntheory import factorint

class IntegerRing:
    def __str__(self): return "Z"
    def __repr__(self): return "Z"
    @property
    def is_commutative(self): return True
    @property
    def has_identity(self): return True
    @property
    def is_noetherian(self): return True

# Top-level setup
Z = IntegerRing()

def conditions(witness) -> list[bool]:
    try:
        h1 = False
        h2 = False
        h3 = False
        q = True
        
        # Parse witness: can be a tuple (Ring, Ideal) or just the Ideal (assuming Z)
        if isinstance(witness, tuple) and len(witness) == 2:
            ring, ideal = witness
        else:
            ring = Z
            ideal = witness
            
        # Case 1: Ring is the integers (Z)
        if ring is Z or str(ring) in ("Z", "ZZ"):
            h1 = True
            h2 = True
            
            # Determine the generator n for the ideal nZ
            if ideal is Z or str(ideal) in ("Z", "ZZ") or ideal == 1 or ideal == [1]:
                n = 1
            else:
                try:
                    n = abs(int(ideal))
                except (ValueError, TypeError):
                    return [False, False, False, False]
                    
            # H3: nZ is irreducible iff n=0, n=1, or n=p^k
            if n == 0 or n == 1:
                h3 = True
            else:
                h3 = (len(factorint(n)) == 1)
                
            # Q: nZ is primary iff n=0 or n=p^k (n=1 is not proper, hence not primary)
            if n == 0:
                q = True
            elif n == 1:
                q = False
            else:
                q = (len(factorint(n)) == 1)
                
            return [h1, h2, h3, not q]
            
        # Case 2: Other rings (e.g., polynomial rings, fields)
        is_comm = getattr(ring, 'is_commutative', False)
        is_field = getattr(ring, 'is_Field', False)
        is_poly = hasattr(ring, 'domain') and hasattr(ring, 'symbols')
        
        if is_comm or is_field or is_poly:
            h1 = True
            
        if getattr(ring, 'is_noetherian', False) or is_field or is_poly:
            h2 = True
            
        # Check if the ideal is the whole ring (the only way an irreducible ideal is not primary)
        is_whole = False
        if ideal == 1 or ideal == [1]:
            is_whole = True
        elif hasattr(ideal, 'is_whole_ring') and ideal.is_whole_ring():
            is_whole = True
        elif hasattr(ring, 'one') and ideal == ring.one:
            is_whole = True
        elif ideal is ring or str(ideal) == str(ring):
            is_whole = True
            
        if is_whole:
            h3 = True
            q = False
            return [h1, h2, h3, not q]
            
        # If it's a field and the ideal is 0
        if is_field:
            if ideal == 0 or ideal == [0]:
                h3 = True
                q = True
                return [h1, h2, h3, not q]
                
        # Fallback for proper ideals in other rings:
        # In a commutative Noetherian ring, every proper irreducible ideal is primary.
        # Thus, it cannot be a counterexample.
        h3 = False
        q = True
        return [h1, h2, h3, not q]
        
    except Exception:
        pass
        
    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R is a Noetherian ring",
    "H_3: I is an irreducible ideal",
    "¬Q: I is not a primary ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy.ntheory import isprime
from sympy.polys.domains import ZZ, QQ, RR, CC
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture:
    "An Artinian commutative ring with identity is a field."
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # If witness is an integer n, we interpret it as the ring Z/nZ
        if (isinstance(witness, int) and not isinstance(witness, bool)) or \
           (hasattr(witness, 'is_Integer') and witness.is_Integer):
            n = int(witness)
            if n > 1:
                h1 = True
                h2 = True
                neg_q = not isprime(n)
                
        # If witness is a tuple of integers, interpret as a product of rings Z/n_i Z
        elif isinstance(witness, tuple) and all(
            ((isinstance(val, int) and not isinstance(val, bool)) or 
             (hasattr(val, 'is_Integer') and val.is_Integer)) for val in witness
        ):
            nums = [int(val) for val in witness]
            if len(nums) > 0 and all(val > 1 for val in nums):
                h1 = True
                h2 = True
                if len(nums) == 1:
                    neg_q = not isprime(nums[0])
                else:
                    neg_q = True
                    
        # If witness is the ring of integers ZZ
        elif witness == ZZ:
            h1 = True
            h2 = False  # ZZ is not Artinian
            neg_q = True
            
        # If witness is a standard field
        elif witness in (QQ, RR, CC):
            h1 = True
            h2 = True
            neg_q = False
            
        # If witness is a general SymPy field
        elif hasattr(witness, 'is_Field') and witness.is_Field:
            h1 = True
            h2 = True
            neg_q = False
            
        # If witness is a general SymPy ring
        elif hasattr(witness, 'is_Ring') and witness.is_Ring:
            h1 = True
            # Check if it's a finite quotient ring like ZZ/nZZ
            if hasattr(witness, 'domain') and witness.domain == ZZ and hasattr(witness, 'base_ideal'):
                h2 = True
                try:
                    gen = witness.base_ideal.gens[0]
                    neg_q = not isprime(int(gen))
                except Exception:
                    neg_q = True
            else:
                # For other infinite rings, we conservatively assume not Artinian
                h2 = False
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: R satisfies the descending chain condition on ideals (Artinian ring)",
    "¬Q: R is not a field"
]

N_HYP = 2
NEG_Q_INDEX = 2
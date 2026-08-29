import math
import re
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "Let R be a commutative ring. There is an R-module isomorphism between 
    the direct sum I \oplus J and the direct sum R \oplus (I \cap J)."
    
    The true theorem requires I and J to be comaximal ideals.
    
    Expected witness formats:
      - Tuple (n, a, b) representing R = Z/nZ, I = (a), J = (b). (n=0 means R = Z)
      - Tuple (a, b) representing R = Z, I = (a), J = (b).
      - Dictionary with keys 'R' (or 'n'), 'a' (or 'I'), 'b' (or 'J').
    """
    try:
        # Parse witness
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R_obj, a_obj, b_obj = witness
            elif len(witness) == 2:
                R_obj = 0
                a_obj, b_obj = witness
            else:
                return [False, False]
        elif isinstance(witness, dict):
            R_obj = witness.get('R', witness.get('n', 0))
            a_obj = witness.get('a', witness.get('I', 0))
            b_obj = witness.get('b', witness.get('J', 0))
        else:
            return [False, False]
            
        # Determine n (modulus of the ring Z/nZ, with n=0 meaning Z or a field)
        R_str = str(R_obj).strip().replace(' ', '')
        if R_str in ["ZZ", "Z", "QQ", "Q", "RR", "R", "CC", "C", "Integers", "Rationals", "Reals", "Complexes"]:
            n = 0
        elif hasattr(R_obj, 'name') and R_obj.name in ["ZZ", "QQ", "RR", "CC"]:
            n = 0
        else:
            try:
                n = int(R_obj)
            except (ValueError, TypeError):
                m = re.search(r'\d+', R_str)
                if m:
                    n = int(m.group())
                else:
                    n = 0
                    
        n = abs(n)
        
        # Determine a and b (generators of the ideals)
        def extract_int(val):
            if isinstance(val, (list, tuple, set)) and len(val) >= 1:
                val = list(val)[0]
            try:
                return int(val)
            except (ValueError, TypeError):
                s = str(val).strip()
                if s in ["Z", "ZZ", "R", "QQ"]:
                    return 1
                m = re.search(r'\d+', s)
                if m:
                    return int(m.group())
                return 0
                
        a = abs(extract_int(a_obj))
        b = abs(extract_int(b_obj))
        
        # H_1: R is a commutative ring
        # Z/nZ (and Z for n=0) is always a commutative ring.
        h1_ok = True
        
        if n == 0:
            # R = Z (or a field, which behaves the same for this rank logic)
            # Any non-zero ideal in Z is isomorphic to Z (rank 1).
            I_rank = 1 if a != 0 else 0
            J_rank = 1 if b != 0 else 0
            I_cap_J_rank = 1 if (a != 0 and b != 0) else 0
            R_rank = 1
            
            IJ_sum_rank = I_rank + J_rank
            R_IcapJ_sum_rank = R_rank + I_cap_J_rank
            
            # Free modules over Z are isomorphic iff they have the same rank
            isomorphic = (IJ_sum_rank == R_IcapJ_sum_rank)
        else:
            # R = Z/nZ
            a_gen = math.gcd(a, n)
            b_gen = math.gcd(b, n)
            
            I_order = n // a_gen
            J_order = n // b_gen
            
            I_cap_J_gen = math.lcm(a_gen, b_gen)
            I_cap_J_order = n // I_cap_J_gen
            
            R_order = n
            
            # For Z/nZ, the modules I ⊕ J and R ⊕ (I ∩ J) are isomorphic 
            # if and only if they have the same number of elements.
            isomorphic = (I_order * J_order == R_order * I_cap_J_order)
            
        # The conclusion FAILS if they are NOT isomorphic
        neg_q_ok = not isomorphic
        
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: I ⊕ J is not isomorphic to R ⊕ (I ∩ J)"
]

N_HYP = 1
NEG_Q_INDEX = 1
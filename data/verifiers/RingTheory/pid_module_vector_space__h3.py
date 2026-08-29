import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to represent an element p in R=Z, and optionally n for M=Z/nZ.
    """
    try:
        p = None
        n = None
        
        # Parse witness
        if isinstance(witness, (tuple, list)):
            if len(witness) >= 2:
                p, n = witness[0], witness[1]
            elif len(witness) == 1:
                p = witness[0]
                n = p
        elif isinstance(witness, dict):
            p = witness.get('p', None)
            n = witness.get('n', p)
        
        if p is None:
            if isinstance(witness, str):
                nums = []
                current_num = ""
                for char in witness:
                    if char.isdigit() or (char == '-' and not current_num):
                        current_num += char
                    else:
                        if current_num not in ("", "-"):
                            nums.append(int(current_num))
                        current_num = ""
                if current_num not in ("", "-"):
                    nums.append(int(current_num))
                    
                if len(nums) >= 2:
                    p, n = nums[0], nums[1]
                elif len(nums) == 1:
                    p = nums[0]
                    n = p
                else:
                    p = witness
                    n = witness
            else:
                p = witness
                n = witness
                
        p_val = int(p)
        n_val = int(n)
        
        # H_1: R is a principal ideal domain
        # We implicitly use R = Z, which is always a PID.
        h1 = True
        
        # H_2: M is a module over R
        # We implicitly use M = Z/nZ, which is always a Z-module.
        h2 = True
        
        # H_3: pM = {0}
        # In Z/nZ, p * x = 0 for all x iff p is a multiple of n.
        h3 = (p_val % n_val == 0) if n_val != 0 else (p_val == 0)
        
        # neg_Q: M is NOT a vector space over the quotient ring R/(p)
        # A vector space must be over a field. R/(p) = Z/pZ is a field iff |p| is prime.
        # If |p| is not prime, R/(p) is not a field, so M cannot be a vector space over it.
        neg_q = not sympy.ntheory.isprime(abs(p_val))
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a module over R",
    "H_3: pM = {0}",
    "¬Q: M is not a vector space over the quotient ring R/(p)"
]

N_HYP = 3
NEG_Q_INDEX = 3
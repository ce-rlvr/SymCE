import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# Since SymPy does not have built-in support for abstract modules over local rings,
# we provide mock objects for the standard counterexample (R = Z_{(p)}, M = Q, N = Q/Z).
class CommutativeLocalRing:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name
    def is_commutative_local_ring(self):
        return True

class Module:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return self.name
    def __repr__(self):
        return self.name

Z_p = CommutativeLocalRing("Z_{(p)}")
Q = Module("Q")
Q_mod_Z = Module("Q/Z")

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative local ring, and M, N are non-zero R-modules, 
    then M \otimes_R N is not the zero module."
    
    A valid counterexample must be a tuple (R, M, N) where:
    - R is a commutative local ring (e.g., Z_{(p)})
    - M is a non-zero module (e.g., Q)
    - N is a non-zero module (e.g., Q/Z)
    - M \otimes_R N = 0 (e.g., Q \otimes_{Z_{(p)}} Q/Z = 0)
    """
    try:
        # Parse the witness
        if isinstance(witness, tuple) and len(witness) == 3:
            R, M, N = witness
        elif isinstance(witness, dict):
            R = witness.get('R', witness.get('ring', ''))
            M = witness.get('M', witness.get('m', ''))
            N = witness.get('N', witness.get('n', ''))
        elif isinstance(witness, str):
            parts = witness.split(',')
            if len(parts) == 3:
                R, M, N = parts
            else:
                R, M, N = witness, witness, witness
        else:
            R, M, N = str(witness), str(witness), str(witness)
            
        r_str = str(R).lower()
        m_str = str(M).lower()
        n_str = str(N).lower()
        
        # H_1: R is a commutative local ring
        h1 = False
        local_keywords = [
            'local', 'z_p', 'z_{(', 'z_(', 'valuation', 'dvr', 
            'power series', '[[x]]', 'p-adic'
        ]
        if any(x in r_str for x in local_keywords):
            h1 = True
        elif hasattr(R, 'is_commutative_local_ring') and R.is_commutative_local_ring():
            h1 = True
            
        # H_2: M is not the zero module
        h2 = False
        if m_str and m_str.strip() not in ['0', 'zero', 'none']:
            h2 = True
            
        # H_3: N is not the zero module
        h3 = False
        if n_str and n_str.strip() not in ['0', 'zero', 'none']:
            h3 = True
            
        # ¬Q: M \otimes_R N is the zero module
        # This happens when one module is divisible and the other is torsion.
        neg_q = False
        
        def is_divisible(s):
            s_clean = ''.join(c if c.isalnum() else ' ' for c in s)
            words = s_clean.split()
            if 'q' in words: return True
            if 'fraction' in s: return True
            if 'divisible' in s: return True
            if '((x))' in s: return True
            if 'k' in words: return True
            return False
            
        def is_torsion(s):
            s_clean = ''.join(c if c.isalnum() else ' ' for c in s)
            words = s_clean.split()
            if 'q' in words and 'z' in words: return True
            if 'torsion' in s: return True
            if 'quotient' in s: return True
            if '((x))' in s and ('/' in s or 'mod' in s): return True
            if 'mod' in s: return True
            if 'k' in words and 'r' in words: return True
            if 'm' in words and 'r' in words: return True
            return False
            
        if (is_divisible(m_str) and is_torsion(n_str)) or (is_divisible(n_str) and is_torsion(m_str)):
            neg_q = True
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative local ring",
    "H_2: M is not the zero module",
    "H_3: N is not the zero module",
    "¬Q: The tensor product M \\otimes_R N is the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3
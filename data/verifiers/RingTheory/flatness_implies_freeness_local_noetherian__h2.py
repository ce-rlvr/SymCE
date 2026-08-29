import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.combinatorics.permutations import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup
class Ring:
    def __init__(self, name, is_commutative=True, is_noetherian=True, is_local=True, is_field=False):
        self.name = name
        self.is_commutative = is_commutative
        self.is_noetherian = is_noetherian
        self.is_local = is_local
        self.is_field = is_field
    def __str__(self):
        return self.name

class Module:
    def __init__(self, name, is_flat=True, is_free=False):
        self.name = name
        self.is_flat = is_flat
        self.is_free = is_free
    def __str__(self):
        return self.name

Z_p = Ring("Z_{(p)}")
Q_mod = Module("Q")

k_x = Ring("k[[x]]")
k_xx = Module("k((x))")

def check_string_witness(s, is_R=False, is_M=False):
    try:
        s_lower = str(s).lower()
        s_clean = str(s).replace(" ", "").lower()
        
        h1 = False
        h2 = False
        neg_q = False
        
        def has_q(text):
            for char in ["=", ",", "'", '"', ":", "(", ")", "[", "]", "{", "}"]:
                text = text.replace(char, " ")
            padded = " " + text + " "
            return " q " in padded or " qq " in padded

        # Check R
        r_patterns = ["z_{p}", "z_{(p)}", "z_(p)", "z_p", "k[[x]]", "k[x]_{x}", "k[x]_{(x)}", "k[x]_(x)"]
        if any(p in s_clean for p in r_patterns):
            h1 = True
        elif "local" in s_lower and "noetherian" in s_lower:
            h1 = True
        elif has_q(s_lower) or "field" in s_clean:
            h1 = True
            
        # Check M
        if has_q(s_lower) or "k((x))" in s_clean or "k(x)" in s_clean:
            h2 = True
        elif "flat" in s_lower:
            h2 = True
            
        # Check neg_Q
        if has_q(s_lower) or "k((x))" in s_clean or "k(x)" in s_clean:
            neg_q = True
        elif "not free" in s_lower or "non-free" in s_lower or "nonfree" in s_lower:
            neg_q = True
            
        # If we know this string represents R, and R is a field, then modules over it are free
        if is_R and (has_q(s_lower) or "field" in s_clean):
            neg_q = False
            
        # If the string contains both R and M
        if not is_R and not is_M:
            # Check if R is explicitly a field
            if "r=q" in s_clean or "r=qq" in s_clean or "r=k((x))" in s_clean or "r=k(x)" in s_clean:
                neg_q = False
                
        return h1, h2, neg_q
    except Exception:
        return False, False, False

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # If witness is a string
        if isinstance(witness, str):
            return list(check_string_witness(witness))
            
        # If witness is a dict
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
        # If witness is a tuple
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
        else:
            R = getattr(witness, 'R', None)
            M = getattr(witness, 'M', None)
            if R is None and M is None:
                # Try string representation
                return list(check_string_witness(str(witness)))

        # Check R
        is_field = False
        if hasattr(R, 'is_commutative') and hasattr(R, 'is_noetherian') and hasattr(R, 'is_local'):
            h1 = bool(R.is_commutative and R.is_noetherian and R.is_local)
            if hasattr(R, 'is_field') and R.is_field:
                is_field = True
        else:
            h1_str, _, _ = check_string_witness(str(R), is_R=True)
            h1 = h1_str
            s_clean = str(R).replace(" ", "").lower()
            padded = str(R).lower()
            for char in ["=", ",", "'", '"', ":", "(", ")", "[", "]", "{", "}"]:
                padded = padded.replace(char, " ")
            padded = " " + padded + " "
            if " q " in padded or " qq " in padded or "field" in s_clean:
                is_field = True

        # Check M
        if hasattr(M, 'is_flat'):
            h2 = bool(M.is_flat)
        else:
            _, h2_str, _ = check_string_witness(str(M), is_M=True)
            h2 = h2_str

        # Check neg_Q
        if hasattr(M, 'is_free'):
            neg_q = not bool(M.is_free)
        else:
            _, _, neg_q_str = check_string_witness(str(M), is_M=True)
            neg_q = neg_q_str
            
        if is_field:
            neg_q = False
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (R, m) is a commutative Noetherian local ring",
    "H_2: M is a flat R-module",
    "¬Q: M is not a free R-module"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
import math
import itertools
import functools

# Top-level setup: named object bindings that the witness expression may reference.
# We provide a simple class hierarchy to represent rings, modules, and subsets
# since SymPy does not have built-in representations for arbitrary modules.

class CommutativeRing:
    def __init__(self, name): 
        self.name = name
    def __repr__(self): 
        return f"Ring({self.name})"

class RModule:
    def __init__(self, name, ring): 
        self.name = name
        self.ring = ring
    def __repr__(self): 
        return f"Module({self.name})"

class MultSubset:
    def __init__(self, name, ring): 
        self.name = name
        self.ring = ring
    def __repr__(self): 
        return f"Subset({self.name})"

# Standard rings
Z = CommutativeRing("Z")
Q = CommutativeRing("Q")

# Standard modules over Z
Mod_Z = RModule("Z", Z)
Mod_Q = RModule("Q", Z)
Mod_Z_N = RModule("Z^N", Z)       # Infinite direct sum of Z
Mod_Z_2 = RModule("Z_2", Z)
Mod_Q_Z = RModule("Q/Z", Z)
Mod_Z_half = RModule("Z[1/2]", Z)

# Standard multiplicatively closed subsets of Z
S_nonzero = MultSubset("Z\\{0}", Z)
S_powers_of_2 = MultSubset("{2^k}", Z)
S_trivial = MultSubset("{1}", Z)

def hom(M, N, R):
    if R == "Z":
        if M == "Q" and N == "Z": return "0"
        if M == "Q" and N == "Q": return "Q"
        if M == "Z" and N == "Z": return "Z"
        if M == "Z" and N == "Q": return "Q"
        if M == "Z^N" and N == "Z": return "Z^N_prod"
        if M == "Z_2" and N == "Z": return "0"
        if M == "Z_2" and N == "Z_2": return "Z_2"
        if M == "Q/Z" and N == "Z": return "0"
        if M == "Z[1/2]" and N == "Z": return "0"
        if M == "0" or N == "0": return "0"
    return None

def localize_module(M, S, R):
    if R == "Z" and S == "Z\\{0}":
        if M == "Z": return "Q"
        if M == "Q": return "Q"
        if M == "0": return "0"
        if M == "Z^N": return "Q^N"
        if M == "Z^N_prod": return "Z^N_prod_otimes_Q"
        if M == "Z_2": return "0"
        if M == "Q/Z": return "0"
        if M == "Z[1/2]": return "Q"
    if R == "Z" and S == "{2^k}":
        if M == "Z": return "Z[1/2]"
        if M == "Q": return "Q"
        if M == "0": return "0"
        if M == "Z_2": return "0"
        if M == "Z[1/2]": return "Z[1/2]"
    if S == "{1}":
        return M
    return None

def localize_ring(R, S):
    if R == "Z" and S == "Z\\{0}": return "Q"
    if R == "Z" and S == "{2^k}": return "Z[1/2]"
    if S == "{1}": return R
    return None

def hom_localized(M_loc, N_loc, R_loc):
    if R_loc == "Q":
        if M_loc == "Q" and N_loc == "Q": return "Q"
        if M_loc == "0" or N_loc == "0": return "0"
        if M_loc == "Q^N" and N_loc == "Q": return "Q^N_prod"
    if R_loc == "Z[1/2]":
        if M_loc == "Z[1/2]" and N_loc == "Z[1/2]": return "Z[1/2]"
        if M_loc == "Q" and N_loc == "Z[1/2]": return "0"
        if M_loc == "0" or N_loc == "0": return "0"
    if R_loc == R_loc and R_loc not in ["Q", "Z[1/2]"]:
        return hom(M_loc, N_loc, R_loc)
    return None

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, M, N, S) or a dict with these keys.
    """
    try:
        if isinstance(witness, dict):
            R_obj = witness.get('R')
            M_obj = witness.get('M')
            N_obj = witness.get('N')
            S_obj = witness.get('S')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            R_obj, M_obj, N_obj, S_obj = witness
        else:
            return [False, False, False, False]
            
        # H1: R is a commutative ring with identity
        if isinstance(R_obj, CommutativeRing):
            h1 = True
            R_name = R_obj.name
        elif isinstance(R_obj, str) and R_obj in ["Z", "Q"]:
            h1 = True
            R_name = R_obj
        else:
            h1 = False
            R_name = str(R_obj)
            
        # H2: N is an R-module
        if isinstance(N_obj, RModule):
            h2 = (N_obj.ring == R_obj) or (N_obj.ring.name == R_name)
            N_name = N_obj.name
        elif isinstance(N_obj, str):
            h2 = True
            N_name = N_obj
        else:
            h2 = False
            N_name = str(N_obj)
            
        # H3: S is a multiplicatively closed subset of R
        if isinstance(S_obj, MultSubset):
            h3 = (S_obj.ring == R_obj) or (S_obj.ring.name == R_name)
            S_name = S_obj.name
        elif isinstance(S_obj, str):
            h3 = True
            S_name = S_obj
        else:
            h3 = False
            S_name = str(S_obj)
            
        # M must also be an R-module for the statement to make sense
        if isinstance(M_obj, RModule):
            is_M_mod = (M_obj.ring == R_obj) or (M_obj.ring.name == R_name)
            M_name = M_obj.name
        elif isinstance(M_obj, str):
            is_M_mod = True
            M_name = M_obj
        else:
            is_M_mod = False
            M_name = str(M_obj)
            
        if not (h1 and h2 and h3 and is_M_mod):
            return [h1, h2, h3, False]
            
        # Evaluate the Hom and localizations
        hom_MN = hom(M_name, N_name, R_name)
        loc_hom = localize_module(hom_MN, S_name, R_name)
        
        loc_M = localize_module(M_name, S_name, R_name)
        loc_N = localize_module(N_name, S_name, R_name)
        R_loc = localize_ring(R_name, S_name)
        
        hom_loc = hom_localized(loc_M, loc_N, R_loc)
        
        # neg_Q: The canonical map is NOT an isomorphism
        if loc_hom is None or hom_loc is None:
            neg_q = False
        else:
            neg_q = (loc_hom != hom_loc)
            
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: N is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The canonical S^{-1}R-module homomorphism from S^{-1}Hom_R(M, N) to Hom_{S^{-1}R}(S^{-1}M, S^{-1}N) is not an isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3
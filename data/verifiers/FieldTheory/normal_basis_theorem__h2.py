import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a counterexample to the false conjecture.
    The true Normal Basis Theorem requires the Galois extension to be FINITE.
    Without the "finite" hypothesis, an infinite Galois extension serves as a counterexample,
    because the Galois orbit of any element is finite (since every element is algebraic and 
    belongs to a finite Galois subextension), and thus its span cannot be the entire 
    infinite-dimensional vector space K over F.
    """
    h1, h2, neg_q = False, False, False
    
    try:
        # 1. Dictionary witness
        if isinstance(witness, dict):
            h1_val = witness.get("is_field_extension", False)
            h1 = bool(h1_val() if callable(h1_val) else h1_val)
            
            h2_val = witness.get("is_galois", False)
            h2 = bool(h2_val() if callable(h2_val) else h2_val)
            
            if "has_normal_basis" in witness:
                nb_val = witness["has_normal_basis"]
                neg_q = not bool(nb_val() if callable(nb_val) else nb_val)
            else:
                inf_val = witness.get("is_infinite", False)
                is_inf = bool(inf_val() if callable(inf_val) else inf_val)
                
                fin_val = witness.get("is_finite", True)
                is_fin = bool(fin_val() if callable(fin_val) else fin_val)
                
                neg_q = is_inf or not is_fin
            return [h1, h2, neg_q]

        # 2. Mock object witness
        if hasattr(witness, "is_field_extension"):
            h1_attr = getattr(witness, "is_field_extension")
            h1 = bool(h1_attr() if callable(h1_attr) else h1_attr)
            
            h2_attr = getattr(witness, "is_galois", False)
            h2 = bool(h2_attr() if callable(h2_attr) else h2_attr)
            
            if hasattr(witness, "has_normal_basis"):
                nb_attr = getattr(witness, "has_normal_basis")
                neg_q = not bool(nb_attr() if callable(nb_attr) else nb_attr)
            else:
                inf_attr = getattr(witness, "is_infinite", False)
                is_inf = bool(inf_attr() if callable(inf_attr) else inf_attr)
                
                fin_attr = getattr(witness, "is_finite", True)
                is_fin = bool(fin_attr() if callable(fin_attr) else fin_attr)
                
                neg_q = is_inf or not is_fin
            return [h1, h2, neg_q]

        # 3. String witness (e.g., "Q_bar/Q")
        if isinstance(witness, str):
            if "/" in witness:
                h1 = True
                K, F = witness.split("/", 1)
                K = K.strip().lower()
                F = F.strip().lower()
                
                # Infinite Galois extensions
                if "bar" in K or "alg" in K or "infty" in K or "closure" in K:
                    h2 = True
                    neg_q = True
                # Finite Galois extensions (e.g., C/R)
                elif K == "c" and F == "r":
                    h2 = True
                    neg_q = False
                # Default fallback for other strings
                else:
                    h2 = True
                    neg_q = False
            return [h1, h2, neg_q]

        # 4. Tuple witness (K, F) representing SymPy domains/fields
        if isinstance(witness, tuple) and len(witness) == 2:
            K, F = witness
            if (hasattr(K, "is_Field") or hasattr(K, "has_assoc_Field")) and \
               (hasattr(F, "is_Field") or hasattr(F, "has_assoc_Field")):
                h1 = True
                # Any finite extension representable in SymPy that is Galois will have a normal basis.
                # Thus, it cannot be a valid counterexample.
                h2 = True 
                neg_q = False
            return [h1, h2, neg_q]

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field extension of F",
    "H_2: The extension K/F is Galois",
    "¬Q: There does not exist an element whose Galois orbit forms a basis for K over F"
]

N_HYP = 2
NEG_Q_INDEX = 2
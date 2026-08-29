import sympy
from sympy import S
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z = S.Integers
Q = S.Rationals
R = S.Reals
C = S.Complexes

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # Case 1: Witness is a tuple (Ring, Ideal)
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, I_obj = witness
            
            if isinstance(R_obj, dict):
                h1 = bool(R_obj.get("is_noetherian", R_obj.get("is_Noetherian", False)))
                is_comm = R_obj.get("is_commutative", None)
            else:
                h1 = bool(getattr(R_obj, "is_noetherian", getattr(R_obj, "is_Noetherian", False)))
                is_comm = getattr(R_obj, "is_commutative", None)
                
            if isinstance(I_obj, dict):
                h2 = bool(I_obj.get("is_proper", I_obj.get("is_proper_ideal", False)))
                q = I_obj.get("is_finite_intersection_of_primary", None)
            else:
                h2 = bool(getattr(I_obj, "is_proper", getattr(I_obj, "is_proper_ideal", False)))
                q = getattr(I_obj, "is_finite_intersection_of_primary", None)
                
            if q is None:
                q = True if is_comm is not False else False
                
            neg_q = not bool(q)
            if is_comm is True:
                neg_q = False

        # Case 2: Witness is a dictionary
        elif isinstance(witness, dict):
            if "ring" in witness and "ideal" in witness:
                R_obj = witness["ring"]
                I_obj = witness["ideal"]
                
                if isinstance(R_obj, dict):
                    h1 = bool(R_obj.get("is_noetherian", R_obj.get("is_Noetherian", False)))
                    is_comm = R_obj.get("is_commutative", None)
                else:
                    h1 = bool(getattr(R_obj, "is_noetherian", getattr(R_obj, "is_Noetherian", False)))
                    is_comm = getattr(R_obj, "is_commutative", None)
                    
                if isinstance(I_obj, dict):
                    h2 = bool(I_obj.get("is_proper", I_obj.get("is_proper_ideal", False)))
                    q = I_obj.get("is_finite_intersection_of_primary", None)
                else:
                    h2 = bool(getattr(I_obj, "is_proper", getattr(I_obj, "is_proper_ideal", False)))
                    q = getattr(I_obj, "is_finite_intersection_of_primary", None)
                    
                if q is None:
                    q = True if is_comm is not False else False
                    
                neg_q = not bool(q)
                if is_comm is True:
                    neg_q = False
            else:
                h1 = bool(witness.get("is_noetherian", witness.get("is_Noetherian", False)))
                h2 = bool(witness.get("is_proper_ideal", witness.get("is_proper", False)))
                is_comm = witness.get("is_commutative", None)
                q = witness.get("is_finite_intersection_of_primary", None)
                
                if q is None:
                    q = True if is_comm is not False else False
                    
                neg_q = not bool(q)
                if is_comm is True:
                    neg_q = False

        # Case 3: Witness is a descriptive string
        elif isinstance(witness, str):
            s = witness.lower()
            h1 = True
            h2 = True
            neg_q = True
            if "commutative" in s and "non" not in s and "not commutative" not in s:
                neg_q = False

        # Case 4: Witness is a custom object
        else:
            h1 = bool(getattr(witness, "is_noetherian", getattr(witness, "is_Noetherian", False)))
            h2 = bool(getattr(witness, "is_proper_ideal", getattr(witness, "is_proper", False)))
            is_comm = getattr(witness, "is_commutative", None)
            q = getattr(witness, "is_finite_intersection_of_primary", None)
            
            if q is None:
                q = True if is_comm is not False else False
                
            neg_q = not bool(q)
            if is_comm is True:
                neg_q = False

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Noetherian ring",
    "H_2: I is a proper ideal of R",
    "¬Q: I cannot be expressed as a finite intersection of primary ideals of R"
]

N_HYP = 2
NEG_Q_INDEX = 2
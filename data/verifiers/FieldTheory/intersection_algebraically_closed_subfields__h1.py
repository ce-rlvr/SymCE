import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: {K_i} is a non-empty family of subfields of E",
    "H_2: each K_i is an algebraically closed field",
    "¬Q: the intersection is not an algebraically closed subfield of E"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1, h2, neg_q = False, False, False
    
    try:
        # Extract list if witness is a tuple (e.g., (E, [K1, K2]))
        witness_list = witness
        if isinstance(witness, tuple):
            for item in witness:
                if isinstance(item, list):
                    witness_list = item
                    break
                    
        if isinstance(witness_list, list) and len(witness_list) >= 1:
            
            # 1. Check for Matrix representation
            # A valid counterexample in M_n(R) consists of subfields R*I + R*J_i isomorphic to C.
            # This requires J_i^2 = -I. The intersection is R*I (not algebraically closed) if J_1 != +/- J_2.
            if all(isinstance(M, sp.Matrix) for M in witness_list):
                n = witness_list[0].shape[0]
                I = sp.eye(n)
                
                is_subfield = True
                for J in witness_list:
                    if J.shape != (n, n):
                        is_subfield = False
                        break
                    diff = J**2 + I
                    if not all(sp.simplify(elem) == 0 for elem in diff):
                        is_subfield = False
                        break
                
                if is_subfield:
                    h1 = True
                    h2 = True
                    
                    if len(witness_list) == 1:
                        neg_q = False
                        return [h1, h2, neg_q]
                    
                    J0 = witness_list[0]
                    intersection_is_R = False
                    for J in witness_list[1:]:
                        diff1 = J - J0
                        diff2 = J + J0
                        if not all(sp.simplify(elem) == 0 for elem in diff1) and \
                           not all(sp.simplify(elem) == 0 for elem in diff2):
                            intersection_is_R = True
                            break
                    
                    neg_q = intersection_is_R
                    return [h1, h2, neg_q]

            # 2. Check for Quaternion representation
            # A valid counterexample in Quaternions consists of subfields R + R*q_i isomorphic to C.
            # This requires q_i to be a pure imaginary unit quaternion.
            if all(type(q).__name__ == 'Quaternion' for q in witness_list):
                is_subfield = True
                for q in witness_list:
                    if sp.simplify(q.a) != 0:
                        is_subfield = False
                        break
                    norm_sq = sp.simplify(q.b**2 + q.c**2 + q.d**2)
                    if norm_sq != 1:
                        is_subfield = False
                        break
                
                if is_subfield:
                    h1 = True
                    h2 = True
                    
                    if len(witness_list) == 1:
                        neg_q = False
                        return [h1, h2, neg_q]
                        
                    q0 = witness_list[0]
                    intersection_is_R = False
                    for q in witness_list[1:]:
                        diff_zero = (sp.simplify(q.b - q0.b) == 0 and 
                                     sp.simplify(q.c - q0.c) == 0 and 
                                     sp.simplify(q.d - q0.d) == 0)
                        sum_zero = (sp.simplify(q.b + q0.b) == 0 and 
                                    sp.simplify(q.c + q0.c) == 0 and 
                                    sp.simplify(q.d + q0.d) == 0)
                        if not (diff_zero or sum_zero):
                            intersection_is_R = True
                            break
                    
                    neg_q = intersection_is_R
                    return [h1, h2, neg_q]
    except Exception:
        pass

    # 3. Duck typing fallback for custom witness objects
    try:
        h1_duck = bool(witness.is_non_empty_family_of_subfields())
        h2_duck = bool(witness.are_subfields_algebraically_closed())
        neg_q_duck = not bool(witness.is_intersection_algebraically_closed())
        return [h1_duck, h2_duck, neg_q_duck]
    except Exception:
        pass

    # 4. Dictionary fallback
    try:
        if isinstance(witness, dict):
            h1_dict = bool(witness.get("is_non_empty_family_of_subfields", False))
            h2_dict = bool(witness.get("are_subfields_algebraically_closed", False))
            neg_q_dict = not bool(witness.get("is_intersection_algebraically_closed", True))
            return [h1_dict, h2_dict, neg_q_dict]
    except Exception:
        pass

    return [h1, h2, neg_q]
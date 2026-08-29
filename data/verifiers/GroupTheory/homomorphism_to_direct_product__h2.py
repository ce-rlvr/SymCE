import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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

def conditions(witness):
    try:
        def extract_group(obj, op_obj):
            if obj is None:
                return [], lambda x, y: x
            if hasattr(obj, 'elements') and hasattr(obj, 'identity'):
                elements = list(obj.elements)
                op = lambda x, y: x * y
                return elements, op
            else:
                elements = list(obj)
                if isinstance(op_obj, dict):
                    op = lambda x, y: op_obj.get((x, y), None)
                else:
                    op = op_obj
                return elements, op

        G, G_op = extract_group(witness.get('G'), witness.get('G_op'))
        H1, H1_op = extract_group(witness.get('H1'), witness.get('H1_op'))
        H2, H2_op = extract_group(witness.get('H2'), witness.get('H2_op'))
        K, K_op = extract_group(witness.get('K'), witness.get('K_op'))
        
        f_obj = witness.get('f')
        if isinstance(f_obj, dict):
            f = lambda x: f_obj.get(x, None)
        else:
            f = f_obj

        def is_group(elements, op):
            if not elements: return False
            elements = list(elements)
            # closure
            for x in elements:
                for y in elements:
                    try:
                        z = op(x, y)
                        if z not in elements: return False
                    except Exception:
                        return False
            # associativity
            for x in elements:
                for y in elements:
                    for z in elements:
                        try:
                            if op(op(x, y), z) != op(x, op(y, z)): return False
                        except Exception:
                            return False
            # identity
            id_elem = None
            for e in elements:
                is_id = True
                for x in elements:
                    try:
                        if op(e, x) != x or op(x, e) != x:
                            is_id = False
                            break
                    except Exception:
                        is_id = False
                        break
                if is_id:
                    id_elem = e
                    break
            if id_elem is None: return False
            # inverses
            for x in elements:
                has_inv = False
                for y in elements:
                    try:
                        if op(x, y) == id_elem and op(y, x) == id_elem:
                            has_inv = True
                            break
                    except Exception:
                        pass
                if not has_inv: return False
            return True

        h1_ok = is_group(G, G_op) and is_group(H1, H1_op) and is_group(H2, H2_op)
        
        h2_ok = is_group(H1, H1_op) and is_group(H2, H2_op)
        
        # Check if f maps G to K
        f_maps_to_K = True
        for x in G:
            try:
                if f(x) not in K:
                    f_maps_to_K = False
                    break
            except Exception:
                f_maps_to_K = False
                break
                
        if not is_group(K, K_op) or not f_maps_to_K:
            f_is_hom = False
        else:
            f_is_hom = True
            for x in G:
                for y in G:
                    try:
                        if f(G_op(x, y)) != K_op(f(x), f(y)):
                            f_is_hom = False
                            break
                    except Exception:
                        f_is_hom = False
                        break
                if not f_is_hom:
                    break
                    
        valid_f_image = True
        for x in G:
            try:
                fx = f(x)
                if not (isinstance(fx, (tuple, list)) and len(fx) == 2 and fx[0] in H1 and fx[1] in H2):
                    valid_f_image = False
                    break
            except Exception:
                valid_f_image = False
                break
                
        if not valid_f_image:
            pi1_f_is_hom = False
            pi2_f_is_hom = False
        else:
            pi1_f_is_hom = True
            for x in G:
                for y in G:
                    try:
                        if f(G_op(x, y))[0] != H1_op(f(x)[0], f(y)[0]):
                            pi1_f_is_hom = False
                            break
                    except Exception:
                        pi1_f_is_hom = False
                        break
                if not pi1_f_is_hom:
                    break
                    
            pi2_f_is_hom = True
            for x in G:
                for y in G:
                    try:
                        if f(G_op(x, y))[1] != H2_op(f(x)[1], f(y)[1]):
                            pi2_f_is_hom = False
                            break
                    except Exception:
                        pi2_f_is_hom = False
                        break
                if not pi2_f_is_hom:
                    break
                    
        neg_q_ok = not (f_is_hom == (pi1_f_is_hom and pi2_f_is_hom))
        
        return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G, H1, and H2 are groups",
    "H_2: pi_1 and pi_2 are canonical projection homomorphisms",
    "¬Q: f is a group homomorphism iff both pi_1 o f and pi_2 o f are group homomorphisms is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2
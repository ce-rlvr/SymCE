import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: M is a torsion R-module",
    "¬Q: The dual module Hom_R(M, R) is not isomorphic to the zero module"
]

N_HYP = 1
NEG_Q_INDEX = 1

class DictWrapper:
    def __init__(self, initial=None):
        self.items_list = initial if initial is not None else []
        
    def copy(self):
        return DictWrapper(list(self.items_list))
        
    def __contains__(self, key):
        for k, v in self.items_list:
            if k == key:
                return True
        return False
        
    def __getitem__(self, key):
        for k, v in self.items_list:
            if k == key:
                return v
        raise KeyError(key)
        
    def __setitem__(self, key, value):
        for i, (k, v) in enumerate(self.items_list):
            if k == key:
                self.items_list[i] = (key, value)
                return
        self.items_list.append((key, value))
        
    def items(self):
        return self.items_list
        
    def values(self):
        return [v for k, v in self.items_list]

def extract_ring_module(witness):
    if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int) and isinstance(witness[1], int):
        n, m = witness
        R = list(range(n))
        M = list(range(m))
        add_R = lambda x, y: (x + y) % n
        mul_R = lambda x, y: (x * y) % n
        add_M = lambda x, y: (x + y) % m
        act_M = lambda r, x: (r * x) % m
        zero_R = 0
        zero_M = 0
        return R, M, add_R, mul_R, add_M, act_M, zero_R, zero_M

    if isinstance(witness, dict):
        if 'R' in witness:
            return (list(witness['R']), list(witness['M']), 
                    witness['add_R'], witness['mul_R'], 
                    witness['add_M'], witness['act_M'], 
                    witness['zero_R'], witness['zero_M'])
        else:
            return (list(witness['R_elements']), list(witness['M_elements']), 
                    witness['add_R'], witness['mul_R'], 
                    witness['add_M'], witness['act_M'], 
                    witness['zero_R'], witness['zero_M'])

    try:
        return (list(witness.R), list(witness.M), 
                witness.add_R, witness.mul_R, 
                witness.add_M, witness.act_M, 
                witness.zero_R, witness.zero_M)
    except AttributeError:
        pass

    try:
        R_obj, M_obj = witness
        return (list(R_obj.elements), list(M_obj.elements), 
                R_obj.add, R_obj.mul, 
                M_obj.add, M_obj.act, 
                R_obj.zero, M_obj.zero)
    except Exception:
        pass

    raise ValueError("Unrecognized witness format")

def check_axioms(R, M, add_R, mul_R, add_M, act_M, zero_R, zero_M):
    for a in R:
        for b in R:
            if add_R(a, b) not in R: return False
            if mul_R(a, b) not in R: return False
            
    for m in M:
        for n in M:
            if add_M(m, n) not in M: return False
    for r in R:
        for m in M:
            if act_M(r, m) not in M: return False
            
    for r1 in R:
        for r2 in R:
            r1r2 = mul_R(r1, r2)
            for m in M:
                if act_M(r1r2, m) != act_M(r1, act_M(r2, m)): return False
                
    for r in R:
        for m1 in M:
            for m2 in M:
                if act_M(r, add_M(m1, m2)) != add_M(act_M(r, m1), act_M(r, m2)): return False
                
    for r1 in R:
        for r2 in R:
            r1_plus_r2 = add_R(r1, r2)
            for m in M:
                if act_M(r1_plus_r2, m) != add_M(act_M(r1, m), act_M(r2, m)): return False
                
    has_one = False
    for e in R:
        is_id = True
        for r in R:
            if mul_R(e, r) != r or mul_R(r, e) != r:
                is_id = False
                break
        if is_id:
            is_unital = True
            for m in M:
                if act_M(e, m) != m:
                    is_unital = False
                    break
            if is_unital:
                has_one = True
                break
    if not has_one:
        return False
        
    return True

def has_nonzero_homomorphism(R, M, add_R, mul_R, add_M, act_M, zero_R, zero_M):
    M_elements = list(M)
    R_elements = list(R)
    
    def search(index, current_f):
        if index == len(M_elements):
            for v in current_f.values():
                if v != zero_R:
                    return True
            return False
            
        m = M_elements[index]
        if m in current_f:
            return search(index + 1, current_f)
            
        for r in R_elements:
            new_f = current_f.copy()
            new_f[m] = r
            
            queue = [m]
            valid = True
            while queue and valid:
                curr_m = queue.pop(0)
                curr_r = new_f[curr_m]
                
                for ring_el in R_elements:
                    next_m = act_M(ring_el, curr_m)
                    next_r = mul_R(ring_el, curr_r)
                    if next_m not in M_elements:
                        valid = False
                        break
                    if next_m in new_f:
                        if new_f[next_m] != next_r:
                            valid = False
                            break
                    else:
                        new_f[next_m] = next_r
                        queue.append(next_m)
                if not valid: break
                
                for known_m, known_r in list(new_f.items()):
                    sum_m = add_M(curr_m, known_m)
                    sum_r = add_R(curr_r, known_r)
                    if sum_m not in M_elements:
                        valid = False
                        break
                    if sum_m in new_f:
                        if new_f[sum_m] != sum_r:
                            valid = False
                            break
                    else:
                        new_f[sum_m] = sum_r
                        queue.append(sum_m)
                        
                    sum_m2 = add_M(known_m, curr_m)
                    sum_r2 = add_R(known_r, curr_r)
                    if sum_m2 not in M_elements:
                        valid = False
                        break
                    if sum_m2 in new_f:
                        if new_f[sum_m2] != sum_r2:
                            valid = False
                            break
                    else:
                        new_f[sum_m2] = sum_r2
                        queue.append(sum_m2)
                        
            if valid:
                if search(index + 1, new_f):
                    return True
                    
        return False

    initial_f = DictWrapper()
    initial_f[zero_M] = zero_R
    return search(0, initial_f)

def conditions(witness) -> list[bool]:
    try:
        R, M, add_R, mul_R, add_M, act_M, zero_R, zero_M = extract_ring_module(witness)
    except Exception:
        return [False, False]

    try:
        if not check_axioms(R, M, add_R, mul_R, add_M, act_M, zero_R, zero_M):
            return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = True
        for m in M:
            is_torsion = False
            for r in R:
                if r != zero_R and act_M(r, m) == zero_M:
                    is_torsion = True
                    break
            if not is_torsion:
                h1 = False
                break
    except Exception:
        h1 = False

    try:
        neg_q = has_nonzero_homomorphism(R, M, add_R, mul_R, add_M, act_M, zero_R, zero_M)
    except Exception:
        neg_q = False

    return [h1, neg_q]
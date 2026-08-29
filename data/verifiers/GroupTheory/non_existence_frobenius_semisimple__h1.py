import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def conditions(witness) -> list[bool]:
    try:
        elements = list(witness.elements)
        id_elem = witness.identity
        
        h1_ok = True
        for x in elements:
            if x == id_elem:
                continue
            
            closure = set()
            for g in elements:
                closure.add(g * x * ~g)
            
            subgrp = set(closure)
            subgrp.add(id_elem)
            while True:
                new_elems = set(a * b for a in subgrp for b in closure)
                new_elems.update(subgrp)
                if len(new_elems) == len(subgrp):
                    break
                subgrp = new_elems
            
            is_abelian = True
            subgrp_list = list(subgrp)
            for i in range(len(subgrp_list)):
                for j in range(i + 1, len(subgrp_list)):
                    if subgrp_list[i] * subgrp_list[j] != subgrp_list[j] * subgrp_list[i]:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
            
            if is_abelian and len(subgrp) > 1:
                h1_ok = False
                break
    except Exception:
        h1_ok = False

    try:
        neg_q_ok = False
        elements = list(witness.elements)
        id_elem = witness.identity
        
        tested_subgroups = []
        
        for x in elements:
            for y in elements:
                H_elems = {id_elem, x, y}
                while True:
                    new_elems = set(a * b for a in H_elems for b in H_elems)
                    if len(new_elems) == len(H_elems):
                        break
                    H_elems = new_elems
                    
                if len(H_elems) <= 1 or len(H_elems) == len(elements):
                    continue
                    
                if H_elems in tested_subgroups:
                    continue
                tested_subgroups.append(H_elems)
                
                is_frobenius_comp = True
                for g in elements:
                    if g in H_elems:
                        continue
                    
                    intersection_size = 0
                    for h in H_elems:
                        ghg = g * h * ~g
                        if ghg in H_elems:
                            intersection_size += 1
                            if intersection_size > 1:
                                break
                    if intersection_size > 1:
                        is_frobenius_comp = False
                        break
                        
                if is_frobenius_comp:
                    neg_q_ok = True
                    break
            if neg_q_ok:
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a semisimple group",
    "¬Q: G is a Frobenius group"
]

N_HYP = 1
NEG_Q_INDEX = 1
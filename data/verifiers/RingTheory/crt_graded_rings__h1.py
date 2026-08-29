import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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
    "H_1: I and J are homogeneous ideals of R",
    "H_2: I and J are comaximal",
    "¬Q: The canonical ring homomorphism from R/(I \\cap J) to R/I \\times R/J is not an isomorphism of graded rings"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            elements = list(witness['elements'])
            I = list(witness['I'])
            J = list(witness['J'])
            add = witness['add']
            mul = witness['mul']
            degree = witness['degree']
            components = witness['components']
        else:
            R_obj = witness.R
            elements = list(R_obj.elements)
            I = list(witness.I)
            J = list(witness.J)
            add = R_obj.add
            mul = R_obj.mul
            degree = R_obj.degree
            components = R_obj.components
    except Exception:
        try:
            I_sym, J_sym = witness
            R_sym = I_sym.ring
            h1 = I_sym.is_homogeneous and J_sym.is_homogeneous
            h2 = (I_sym + J_sym).contains(R_sym.one)
            return [bool(h1), bool(h2), False]
        except Exception:
            return [False, False, False]

    def is_ideal(ideal):
        if not ideal: return False
        for x in ideal:
            for y in ideal:
                if add(x, y) not in ideal: 
                    return False
        for x in ideal:
            for r in elements:
                if mul(r, x) not in ideal: 
                    return False
                if mul(x, r) not in ideal: 
                    return False
        return True

    def is_homogeneous(ideal):
        for x in ideal:
            comps = components(x)
            for c in comps:
                if c not in ideal: 
                    return False
        return True

    try:
        h1 = is_ideal(I) and is_ideal(J) and is_homogeneous(I) and is_homogeneous(J)
    except Exception:
        h1 = False

    try:
        sums = []
        for i in I:
            for j in J:
                sums.append(add(i, j))
        h2 = True
        for r in elements:
            if r not in sums:
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        I_cap_J = [x for x in I if x in J]
        
        def eq_mod(x, y, ideal):
            for i in ideal:
                if x == add(y, i): 
                    return True
            return False

        cosets_I = []
        for r in elements:
            if not any(eq_mod(r, c[0], I) for c in cosets_I):
                cosets_I.append([x for x in elements if eq_mod(x, r, I)])
                
        cosets_J = []
        for r in elements:
            if not any(eq_mod(r, c[0], J) for c in cosets_J):
                cosets_J.append([x for x in elements if eq_mod(x, r, J)])
                
        cosets_IJ = []
        for r in elements:
            if not any(eq_mod(r, c[0], I_cap_J) for c in cosets_IJ):
                cosets_IJ.append([x for x in elements if eq_mod(x, r, I_cap_J)])
                
        is_iso = True
        
        if len(cosets_IJ) != len(cosets_I) * len(cosets_J):
            is_iso = False
        else:
            degrees = set()
            for r in elements:
                try:
                    d = degree(r)
                    if d is not None:
                        degrees.add(d)
                except Exception:
                    pass
            
            for d in degrees:
                R_d = [r for r in elements if degree(r) == d]
                
                R_I_d = []
                for c in cosets_I:
                    if any(x in R_d for x in c):
                        R_I_d.append(c)
                        
                R_J_d = []
                for c in cosets_J:
                    if any(x in R_d for x in c):
                        R_J_d.append(c)
                        
                R_IJ_d = []
                for c in cosets_IJ:
                    if any(x in R_d for x in c):
                        R_IJ_d.append(c)
                        
                image_pairs = set()
                for x in R_d:
                    c_I_idx = next(i for i, c in enumerate(R_I_d) if x in c)
                    c_J_idx = next(i for i, c in enumerate(R_J_d) if x in c)
                    image_pairs.add((c_I_idx, c_J_idx))
                    
                if len(image_pairs) != len(R_I_d) * len(R_J_d) or len(R_IJ_d) != len(R_I_d) * len(R_J_d):
                    is_iso = False
                    break
                    
        neg_q = not is_iso
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]
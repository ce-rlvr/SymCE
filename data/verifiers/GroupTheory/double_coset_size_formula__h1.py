import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard groups and matrices
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
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
        G, H, K, x = witness
    except Exception:
        return [False, False, False, False]
        
    def get_elems(obj):
        if hasattr(obj, 'elements'):
            elems = list(obj.elements)
        elif hasattr(obj, 'generate'):
            elems = list(obj.generate())
        else:
            elems = list(obj)
        res = []
        for e in elems:
            if hasattr(e, 'as_immutable'):
                res.append(e.as_immutable())
            elif isinstance(e, sympy.Matrix):
                res.append(sympy.ImmutableMatrix(e))
            else:
                res.append(e)
        return res

    def is_subgroup(sub, group):
        if hasattr(sub, 'is_subgroup'):
            try:
                return sub.is_subgroup(group)
            except Exception:
                pass
        if hasattr(sub, 'is_subgroup_of'):
            try:
                return sub.is_subgroup_of(group)
            except Exception:
                pass
                
        try:
            sub_elems = get_elems(sub)
            group_elems = get_elems(group)
            
            # Check subset
            for s in sub_elems:
                if s not in group_elems:
                    return False
                        
            # Check closure and inverses
            sub_set = set(sub_elems)
            if len(sub_set) == 0:
                return False
            for a in sub_set:
                for b in sub_set:
                    prod = a * b
                    if hasattr(prod, 'as_immutable'):
                        prod = prod.as_immutable()
                    if prod not in sub_set:
                        return False
                if hasattr(a, 'inv'):
                    inv = a.inv()
                else:
                    inv = a**-1
                if hasattr(inv, 'as_immutable'):
                    inv = inv.as_immutable()
                if inv not in sub_set:
                    return False
            return True
        except Exception:
            return False

    h1 = is_subgroup(H, G)
    h2 = is_subgroup(K, G)
    
    try:
        if hasattr(x, 'as_immutable'):
            x_imm = x.as_immutable()
        elif isinstance(x, sympy.Matrix):
            x_imm = sympy.ImmutableMatrix(x)
        else:
            x_imm = x
            
        h3 = False
        if hasattr(G, '__contains__') or hasattr(G, 'contains'):
            try:
                if hasattr(G, 'contains'):
                    h3 = G.contains(x)
                else:
                    h3 = x in G
            except Exception:
                pass
            if not h3:
                try:
                    if hasattr(G, 'contains'):
                        h3 = G.contains(x_imm)
                    else:
                        h3 = x_imm in G
                except Exception:
                    pass
        else:
            group_elems = get_elems(G)
            h3 = x_imm in group_elems or x in group_elems
    except Exception:
        h3 = False
        
    try:
        invertible = True
        try:
            if hasattr(x_imm, 'inv'):
                x_inv = x_imm.inv()
            else:
                x_inv = x_imm**-1
            if hasattr(x_inv, 'as_immutable'):
                x_inv = x_inv.as_immutable()
        except Exception:
            invertible = False
            
        if not invertible:
            neg_Q = True
        else:
            H_elems = get_elems(H)
            K_elems = get_elems(K)
            
            size_H = len(H_elems)
            size_K = len(K_elems)
            
            HxK = set()
            for h in H_elems:
                for k in K_elems:
                    prod = h * x_imm * k
                    if hasattr(prod, 'as_immutable'):
                        prod = prod.as_immutable()
                    HxK.add(prod)
            size_HxK = len(HxK)
            
            xKx_inv = set()
            for k in K_elems:
                prod = x_imm * k * x_inv
                if hasattr(prod, 'as_immutable'):
                    prod = prod.as_immutable()
                xKx_inv.add(prod)
                
            H_set = set(H_elems)
            size_int = len(H_set.intersection(xKx_inv))
            
            if size_int == 0:
                formula_val = sympy.oo
            else:
                formula_val = sympy.Rational(size_H * size_K, size_int)
                
            if size_HxK == formula_val:
                neg_Q = False
            else:
                if hasattr(size_HxK, 'equals') and size_HxK.equals(formula_val):
                    neg_Q = False
                else:
                    neg_Q = True
                    
    except Exception:
        try:
            if hasattr(witness, 'size_HxK'):
                size_HxK = witness.size_HxK
                size_H = witness.size_H
                size_K = witness.size_K
                size_int = witness.size_intersection
                
                if size_int == 0:
                    formula_val = sympy.oo
                else:
                    formula_val = sympy.Rational(size_H * size_K, size_int)
                    
                if size_HxK == formula_val:
                    neg_Q = False
                elif size_HxK == sympy.oo and formula_val == sympy.nan:
                    neg_Q = True
                else:
                    neg_Q = True
            else:
                neg_Q = False
        except Exception:
            neg_Q = False
            
    return [bool(h1), bool(h2), bool(h3), bool(neg_Q)]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: K is a subgroup of G",
    "H_3: x is an element of G",
    "¬Q: The cardinality of the double coset H x K is not equal to |H| |K| / |H \\cap x K x^{-1}|"
]

N_HYP = 3
NEG_Q_INDEX = 3
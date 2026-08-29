import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros
import math

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
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is finite and equal to n",
    "¬Q: There is no normal subgroup N of G contained in H such that the index of N in G divides n factorial"
]
N_HYP = 2
NEG_Q_INDEX = 2

def check_h1(G, H):
    try:
        if hasattr(H, 'is_subgroup') and H.is_subgroup(G):
            return True
    except Exception:
        pass
    try:
        for g in H.generators:
            if not G.contains(g):
                return False
        return True
    except Exception:
        return False

def check_h2(G, H, n_val, h1_ok):
    try:
        if not h1_ok:
            return False, None
        actual_n = G.order() // H.order()
        if n_val is not None:
            if actual_n == n_val:
                return True, actual_n
            else:
                return False, actual_n
        else:
            return True, actual_n
    except Exception:
        return False, None

def check_neg_q(G, H, n, h1_ok, h2_ok):
    try:
        if not (h1_ok and h2_ok):
            return False
            
        n_fact = math.factorial(n)
        
        if hasattr(G, 'normal_subgroups'):
            try:
                for N in G.normal_subgroups():
                    contained = True
                    for gen in N.generators:
                        if not H.contains(gen):
                            contained = False
                            break
                    if contained:
                        index_N = G.order() // N.order()
                        if n_fact % index_N == 0:
                            return False
                return True
            except Exception:
                pass
                
        try:
            H_elems = set(H.generate())
            G_elems = list(G.generate())
            core_elems = H_elems
            for g in G_elems:
                conj = {g * h * ~g for h in H_elems}
                core_elems = core_elems.intersection(conj)
            
            index_N = G.order() // len(core_elems)
            if n_fact % index_N == 0:
                return False
            return True
        except Exception:
            pass
            
        return False
    except Exception:
        return False

def conditions(witness):
    if isinstance(witness, tuple):
        if len(witness) == 2:
            G, H = witness
            n_val = None
        elif len(witness) == 3:
            G, H, n_val = witness
        else:
            return [False, False, False]
    else:
        return [False, False, False]
        
    h1 = check_h1(G, H)
    h2, n = check_h2(G, H, n_val, h1)
    neg_q = check_neg_q(G, H, n, h1, h2)
    
    return [h1, h2, neg_q]
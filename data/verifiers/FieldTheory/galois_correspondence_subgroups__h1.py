import sympy
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for potential witness expressions
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

def _get_list(obj):
    if hasattr(obj, 'elements'):
        return list(obj.elements)
    elif hasattr(obj, 'generate'):
        return list(obj.generate())
    return list(obj)

def conditions(witness) -> list[bool]:
    # Extract components from the witness
    try:
        if isinstance(witness, dict):
            L = set(witness.get('L', []))
            K = set(witness.get('K', []))
            G = _get_list(witness.get('G', []))
            H = _get_list(witness.get('H', []))
            M = set(witness.get('M', []))
            Aut_L = _get_list(witness.get('Aut_L', []))
        elif isinstance(witness, tuple) and len(witness) == 6:
            L = set(witness[0])
            K = set(witness[1])
            G = _get_list(witness[2])
            H = _get_list(witness[3])
            M = set(witness[4])
            Aut_L = _get_list(witness[5])
        else:
            L = set(getattr(witness, 'L', []))
            K = set(getattr(witness, 'K', []))
            G = _get_list(getattr(witness, 'G', []))
            H = _get_list(getattr(witness, 'H', []))
            M = set(getattr(witness, 'M', []))
            Aut_L = _get_list(getattr(witness, 'Aut_L', []))
    except Exception:
        return [False, False, False]

    # H_1: H is a subgroup of G
    try:
        h1_ok = True
        G_set = set(G)
        for h in H:
            if h not in G_set:
                h1_ok = False
                break
        if h1_ok and len(H) > 0:
            H_set = set(H)
            for h1 in H:
                for h2 in H:
                    if h1 * h2 not in H_set:
                        h1_ok = False
                        break
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H_2: M is the fixed field of H (M = L^H)
    try:
        fixed_by_H = set()
        for x in L:
            is_fixed = True
            for h in H:
                if h(x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                fixed_by_H.add(x)
        h2_ok = (M == fixed_by_H)
    except Exception:
        h2_ok = False

    # neg_Q: M is not an intermediate field of L/K, or L/M is not Galois, or Gal(L/M) != H
    try:
        # Check if M is an intermediate field of L/K
        M_is_intermediate = K.issubset(M) and M.issubset(L)
        
        # Compute Gal(L/M) as the set of automorphisms in Aut_L fixing M pointwise
        Gal_L_M = []
        for g in Aut_L:
            is_fixed = True
            for x in M:
                if g(x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                Gal_L_M.append(g)
                
        # Check if L/M is Galois (i.e., M is exactly the fixed field of Gal(L/M))
        fixed_by_Gal = set()
        for x in L:
            is_fixed = True
            for g in Gal_L_M:
                if g(x) != x:
                    is_fixed = False
                    break
            if is_fixed:
                fixed_by_Gal.add(x)
                
        L_M_is_Galois = (M == fixed_by_Gal)
        
        # Check if Gal(L/M) == H
        Gal_L_M_equals_H = (set(Gal_L_M) == set(H))
        
        Q = M_is_intermediate and L_M_is_Galois and Gal_L_M_equals_H
        neg_q = not Q
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: M is the fixed field of H",
    "¬Q: M is not an intermediate field of L/K, or L/M is not Galois, or Gal(L/M) != H"
]

N_HYP = 2
NEG_Q_INDEX = 2
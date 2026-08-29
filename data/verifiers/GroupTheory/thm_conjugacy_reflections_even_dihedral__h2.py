import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
        if isinstance(witness, dict):
            G = witness['G']
            n = witness['n']
            R = witness['R']
            rotations = witness.get('rotations', set())
        elif isinstance(witness, (tuple, list)):
            G = witness[0]
            n = witness[1]
            R = witness[2]
            rotations = witness[3] if len(witness) > 3 else set()
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: n is an even positive integer
    try:
        h1 = isinstance(n, int) and n > 0 and n % 2 == 0
    except Exception:
        h1 = False

    # H_2: R is the set of all reflections (elements of order 2 that are not rotations) in G
    try:
        R_set = set(R)
        rotations_set = set(rotations)
        
        expected_R = set()
        for g in G.elements:
            if g.order() == 2 and g not in rotations_set:
                expected_R.add(g)
                
        h2 = (R_set == expected_R)
    except Exception:
        h2 = False

    # neg_Q: R is NOT the disjoint union of exactly two conjugacy classes in G
    try:
        R_set = set(R)
        classes_in_R = []
        unseen = set(R_set)
        neg_q = False
        
        while unseen:
            elem = unseen.pop()
            cclass = set()
            for g in G.elements:
                conj = g * elem * ~g
                cclass.add(conj)
            
            if not cclass.issubset(R_set):
                neg_q = True
                break
                
            classes_in_R.append(cclass)
            unseen -= cclass
            
        if not neg_q:
            if len(classes_in_R) != 2:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an even positive integer",
    "H_2: R is the set of all reflections (elements of order 2 that are not rotations) in G",
    "¬Q: R is not the disjoint union of exactly two conjugacy classes in G"
]

N_HYP = 2
NEG_Q_INDEX = 2
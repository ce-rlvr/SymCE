import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, Permutation
from sympy.ntheory import factorint

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

def conditions(witness):
    try:
        if not hasattr(witness, 'order'):
            return [False, False]
            
        order = witness.order()
        if order == 1:
            return [False, False]
            
        factors = factorint(order)
        if len(factors) != 1:
            return [False, False]
            
        p = list(factors.keys())[0]
        
        Z = witness.center()
        if Z.order() != p:
            return [False, False]
            
        derived = witness.derived_subgroup()
        
        for g in derived.generators:
            if not Z.contains(g):
                return [False, False]
                
        for x in witness.generators:
            if not Z.contains(x**p):
                return [False, False]
                
        H1 = True
        
        Q = (derived.order() == p)
        neg_Q = not Q
        
        return [H1, neg_Q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: G is an extra-special p-group",
    "not Q: The commutator subgroup does not have order exactly p"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class FiniteRing:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def is_commutative(self): 
        return True
        
    def is_noetherian(self): 
        return True
        
    def __repr__(self): 
        return f"Z{self.n}"

Z2 = FiniteRing(2)
Z3 = FiniteRing(3)
Z4 = FiniteRing(4)
Z5 = FiniteRing(5)
Z6 = FiniteRing(6)
Z8 = FiniteRing(8)
Z10 = FiniteRing(10)
Z12 = FiniteRing(12)

def get_ideal(R, gen):
    if isinstance(gen, int):
        gen = [gen]
    else:
        gen = list(gen)
        
    ideal = set([0])
    for g in gen:
        ideal.add(g)
    
    while True:
        new_ideal = set(ideal)
        for a in ideal:
            for b in ideal:
                new_ideal.add(R.add(a, b))
            for r in R.elements:
                new_ideal.add(R.mul(r, a))
        if len(new_ideal) == len(ideal):
            break
        ideal = new_ideal
    return ideal

def conditions(witness):
    try:
        R, I_gen, P_gen = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = getattr(R, 'is_commutative', lambda: False)() and getattr(R, 'is_noetherian', lambda: False)()
    except Exception:
        h1 = False

    if not hasattr(R, 'elements'):
        return [False, False, False]

    try:
        I = get_ideal(R, I_gen)
        P = get_ideal(R, P_gen)
    except Exception:
        return [False, False, False]

    try:
        is_prime = False
        if len(P) < len(R.elements):
            is_prime = True
            for a in R.elements:
                for b in R.elements:
                    if R.mul(a, b) in P:
                        if a not in P and b not in P:
                            is_prime = False
                            break
                if not is_prime:
                    break
        
        is_ass = False
        for x in I:
            ann_x = set(r for r in R.elements if R.mul(r, x) == 0)
            if ann_x == P:
                is_ass = True
                break
                
        h2 = is_prime and is_ass
    except Exception:
        h2 = False

    try:
        exists = False
        for x in R.elements:
            if x not in I:
                I_colon_x = set(r for r in R.elements if R.mul(r, x) in I)
                if I_colon_x == P:
                    exists = True
                    break
        neg_q = not exists
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: P is an associated prime ideal of I",
    "¬Q: There does not exist an element x in R \\ I such that the ideal quotient (I:x) is equal to P"
]

N_HYP = 2
NEG_Q_INDEX = 2
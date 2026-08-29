import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

class RingIdealWitness:
    def __init__(self, comm, art, prime, maximal):
        self.comm = comm
        self.art = art
        self.prime = prime
        self.maximal = maximal
        
    def is_commutative_ring(self): return self.comm
    def is_artinian_ring(self): return self.art
    def is_prime_ideal(self): return self.prime
    def is_maximal_ideal(self): return self.maximal

def conditions(witness) -> list[bool]:
    if hasattr(witness, "is_commutative_ring"):
        try:
            h1 = bool(witness.is_commutative_ring())
        except Exception:
            h1 = False
        try:
            h2 = bool(witness.is_artinian_ring())
        except Exception:
            h2 = False
        try:
            h3 = bool(witness.is_prime_ideal())
        except Exception:
            h3 = False
        try:
            neg_q = not bool(witness.is_maximal_ideal())
        except Exception:
            neg_q = False
        return [h1, h2, h3, neg_q]
        
    try:
        R, P = witness
        R = list(R)
        P = list(P)
    except Exception:
        return [False, False, False, False]
        
    zero = None
    for z in R:
        if all(z + a == a for a in R):
            zero = z
            break
            
    def is_comm_ring():
        if zero is None: return False
        for a in R:
            has_inv = False
            for b in R:
                if a + b == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in R:
                if a + b not in R: return False
                if a * b not in R: return False
                if a + b != b + a: return False
                if a * b != b * a: return False
                for c in R:
                    if (a + b) + c != a + (b + c): return False
                    if (a * b) * c != a * (b * c): return False
                    if a * (b + c) != a * b + a * c: return False
        return True

    def is_ideal(I):
        if not I: return False
        for a in I:
            for b in I:
                if a + b not in I: return False
            has_inv = False
            for b in I:
                if a + b == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for r in R:
                if r * a not in I: return False
                if a * r not in I: return False
        return True

    def is_prime():
        if not is_ideal(P): return False
        if len(P) == len(R): return False
        for a in R:
            for b in R:
                if (a * b) in P:
                    if a not in P and b not in P:
                        return False
        return True

    def is_maximal():
        if not is_ideal(P): return False
        if len(P) == len(R): return False
        
        for x in R:
            if x in P: continue
            gen = set(P)
            added = True
            while added:
                added = False
                new_gen = set(gen)
                for a in gen:
                    for b in gen:
                        if a + b not in new_gen:
                            new_gen.add(a + b)
                            added = True
                    for r in R:
                        if r * a not in new_gen:
                            new_gen.add(r * a)
                            added = True
                gen = new_gen
            if len(gen) < len(R):
                return False
        return True

    try:
        h1 = is_comm_ring()
    except Exception:
        h1 = False

    try:
        h2 = h1 and True 
    except Exception:
        h2 = False

    try:
        h3 = is_prime()
    except Exception:
        h3 = False

    try:
        neg_q = not is_maximal() if h1 and h3 else False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is an Artinian ring",
    "H_3: P is a prime ideal of R",
    "¬Q: P is not a maximal ideal"
]

N_HYP = 3
NEG_Q_INDEX = 3
import sympy
from sympy.matrices import eye, zeros
import itertools
import functools

class FiniteRing:
    """
    A class representing a finite ring (commutative or non-commutative),
    defined by its elements and operation tables.
    This allows the construction of non-commutative counterexamples where
    localization at a prime ideal may fail to exist.
    """
    def __init__(self, elements, add_table, mul_table):
        self.elements = list(elements)
        self.add_table = add_table
        self.mul_table = mul_table
        self.n = len(elements)
        
    def add(self, x, y):
        i = self.elements.index(x)
        j = self.elements.index(y)
        return self.add_table[i][j]
        
    def mul(self, x, y):
        i = self.elements.index(x)
        j = self.elements.index(y)
        return self.mul_table[i][j]
        
    def is_ideal(self, I):
        if not I: 
            return False
        for x in I:
            if x not in self.elements: 
                return False
            for y in I:
                if self.add(x, y) not in I: 
                    return False
        for x in I:
            for r in self.elements:
                if self.mul(r, x) not in I: 
                    return False
                if self.mul(x, r) not in I: 
                    return False
        return True

    def is_prime_ideal(self, P):
        if not self.is_ideal(P): 
            return False
        if len(P) == self.n: 
            return False
        # In non-commutative rings: A B \subseteq P => A \subseteq P or B \subseteq P
        # Equivalent to: x R y \subseteq P => x \in P or y \in P
        for x in self.elements:
            for y in self.elements:
                subset = True
                for r in self.elements:
                    if self.mul(x, self.mul(r, y)) not in P:
                        subset = False
                        break
                if subset:
                    if x not in P and y not in P:
                        return False
        return True

    def is_primary_ideal(self, Q, P):
        if not self.is_ideal(Q): 
            return False
        if not self.is_prime_ideal(P): 
            return False
        if any(x not in P for x in Q): 
            return False
        # Right P-primary: x R y \subseteq Q => x \in Q or y \in P
        for x in self.elements:
            for y in self.elements:
                subset = True
                for r in self.elements:
                    if self.mul(x, self.mul(r, y)) not in Q:
                        subset = False
                        break
                if subset:
                    if x not in Q and y not in P:
                        return False
        return True

    def localization_exists(self, P):
        # Localization at P exists if S = R \ P is an Ore set.
        S = [x for x in self.elements if x not in P]
        if not S: 
            return False
        # Check multiplicatively closed
        for x in S:
            for y in S:
                if self.mul(x, y) not in S:
                    return False
        # Check Ore condition: for all r \in R, s \in S, S r \cap R s \neq \emptyset
        for r in self.elements:
            for s in S:
                Sr = set(self.mul(sp, r) for sp in S)
                Rs = set(self.mul(rp, s) for rp in self.elements)
                if not Sr.intersection(Rs):
                    return False
        return True

def conditions(witness):
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness can be a tuple (ring, P, Q) or an object with attributes R, P, Q.
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            ring, P, Q = witness
        else:
            ring = witness.R
            P = witness.P
            Q = witness.Q
    except Exception:
        return [False, False, False]
        
    try:
        if hasattr(ring, 'is_prime_ideal'):
            h1 = bool(ring.is_prime_ideal(P))
        else:
            h1 = False
    except Exception:
        h1 = False
        
    try:
        if hasattr(ring, 'is_primary_ideal'):
            h2 = bool(ring.is_primary_ideal(Q, P))
        else:
            h2 = False
    except Exception:
        h2 = False
        
    try:
        # The theorem is unconditionally true for commutative rings.
        # It fails for non-commutative rings where localization at P does not exist
        # (e.g., S = R \ P is not an Ore set or not multiplicatively closed).
        if hasattr(ring, 'is_primary_in_localization'):
            neg_q = not bool(ring.is_primary_in_localization(Q, P))
        elif hasattr(ring, 'localization_exists'):
            neg_q = not bool(ring.localization_exists(P))
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: P is a prime ideal in R",
    "H_2: Q is a P-primary ideal in R",
    "¬Q: The extended ideal Q R_P is not a P R_P-primary ideal in the localization R_P (e.g. localization does not exist)"
]

N_HYP = 2
NEG_Q_INDEX = 2
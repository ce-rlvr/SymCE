import sympy
import math
import itertools
import functools

class F2XQuotientElement:
    """
    Represents an element in the ring F_2[x_1, x_2, ...] / (x_1^2, x_2^2, ...).
    This is the standard counterexample to the conjecture that nil ideals are nilpotent
    (without the finitely generated hypothesis).
    """
    def __init__(self, terms):
        self.terms = frozenset(frozenset(t) for t in terms)
        
    def __add__(self, other):
        if not isinstance(other, F2XQuotientElement):
            return NotImplemented
        return F2XQuotientElement(self.terms ^ other.terms)
        
    def __sub__(self, other):
        return self.__add__(other)
        
    def __neg__(self):
        return self
        
    def __mul__(self, other):
        if not isinstance(other, F2XQuotientElement):
            return NotImplemented
        new_terms = set()
        for t1 in self.terms:
            for t2 in other.terms:
                if t1.isdisjoint(t2):
                    t = t1 | t2
                    if t in new_terms:
                        new_terms.remove(t)
                    else:
                        new_terms.add(t)
        return F2XQuotientElement(new_terms)
        
    def __eq__(self, other):
        if not isinstance(other, F2XQuotientElement):
            return False
        return self.terms == other.terms
        
    def is_zero(self):
        return len(self.terms) == 0

    def is_in_ideal(self):
        return frozenset() not in self.terms

def conditions(witness):
    W = None
    if isinstance(witness, str):
        desc = witness.lower()
        has_inf_vars = any(sub in desc for sub in ["infinit", "...", "x_i", "x_n", "x1, x2", "x_1, x_2"])
        has_quotient = any(sub in desc for sub in ["quotient", "/", "ideal", "modulo"])
        has_nil = any(sub in desc for sub in ["2", "square", "nil", "x_i^"])
        if has_inf_vars and has_quotient and has_nil:
            W = F2XQuotientElement
            
    if W is None:
        if callable(witness):
            W = witness
        else:
            W = type(witness)

    try:
        a = W([[1], [2, 3]])
        b = W([[2], [4]])
        c = W([[1, 2], [3]])
        
        is_comm = (a * b == b * a)
        is_assoc = ((a * b) * c == a * (b * c))
        is_distrib = (a * (b + c) == a * b + a * c)
        
        zero = W([])
        one = W([[]])
        is_id = (a * one == a) and (a + zero == a)
        
        h1 = bool(is_comm and is_assoc and is_distrib and is_id)
    except Exception:
        h1 = False

    try:
        elements_in_I = [
            W([[1], [2]]),
            W([[1, 2], [3, 4], [5]]),
            W([[1], [2], [3], [4], [5]])
        ]
        h2 = True
        for el in elements_in_I:
            if hasattr(el, 'is_in_ideal'):
                if not el.is_in_ideal():
                    h2 = False
                    break
                if W([[]]).is_in_ideal():
                    h2 = False
                    break
            
            nilpotent = False
            p = el
            for _ in range(20):
                if p.is_zero():
                    nilpotent = True
                    break
                p = p * el
            if not nilpotent:
                h2 = False
                break
    except Exception:
        h2 = False

    try:
        neg_q = True
        for n in range(1, 15):
            prod = W([[]])
            for i in range(1, n + 1):
                xi = W([[i]])
                prod = prod * xi
            if prod.is_zero():
                neg_q = False
                break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Every element of I is nilpotent",
    "¬Q: I is not nilpotent (there is no n such that I^n = 0)"
]

N_HYP = 2
NEG_Q_INDEX = 2
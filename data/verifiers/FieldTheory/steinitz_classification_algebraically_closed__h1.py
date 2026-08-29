import sympy
import math
import itertools
import functools

class TestField:
    def __init__(self, name, char, tr_deg, iso_class):
        self.name = name
        self.char = char
        self.tr_deg = tr_deg
        self.iso_class = iso_class
        
    def __repr__(self):
        return self.name

QQ = TestField("QQ", 0, 0, "QQ")
QQ_sqrt2 = TestField("QQ(sqrt(2))", 0, 0, "QQ(sqrt(2))")
QQ_sqrt3 = TestField("QQ(sqrt(3))", 0, 0, "QQ(sqrt(3))")
RR = TestField("RR", 0, "c", "RR")
CC = TestField("CC", 0, "c", "CC")
GF2 = TestField("GF(2)", 2, 0, "GF(2)")
GF3 = TestField("GF(3)", 3, 0, "GF(3)")
GF4 = TestField("GF(4)", 2, 0, "GF(4)")
GF8 = TestField("GF(8)", 2, 0, "GF(8)")
GF9 = TestField("GF(9)", 3, 0, "GF(9)")
QQ_t = TestField("QQ(t)", 0, 1, "QQ(t)")
CC_t = TestField("CC(t)", 0, "c", "CC(t)")
GF2_t = TestField("GF(2)(t)", 2, 1, "GF(2)(t)")
GF3_t = TestField("GF(3)(t)", 3, 1, "GF(3)(t)")

_fields = {
    "QQ": QQ,
    "QQ(sqrt(2))": QQ_sqrt2,
    "QQ(sqrt(3))": QQ_sqrt3,
    "RR": RR,
    "CC": CC,
    "GF(2)": GF2,
    "GF(3)": GF3,
    "GF(4)": GF4,
    "GF(8)": GF8,
    "GF(9)": GF9,
    "QQ(t)": QQ_t,
    "CC(t)": CC_t,
    "GF(2)(t)": GF2_t,
    "GF(3)(t)": GF3_t
}

def conditions(witness):
    try:
        K, L = witness
        if isinstance(K, str):
            K = _fields[K]
        if isinstance(L, str):
            L = _fields[L]
            
        same_char = (K.char == L.char)
        same_tr_deg = (K.tr_deg == L.tr_deg)
        isomorphic = (K.iso_class == L.iso_class)
        
        conjecture_holds = (isomorphic == (same_char and same_tr_deg))
        neg_Q = not conjecture_holds
    except Exception:
        neg_Q = False
        
    return [neg_Q]

CONDITION_LABELS = [
    "¬Q: The biconditional (K isomorphic to L <=> same char and same tr_deg) fails"
]

N_HYP = 0
NEG_Q_INDEX = 0
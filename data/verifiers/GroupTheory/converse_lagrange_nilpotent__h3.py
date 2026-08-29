import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.ntheory import factorint
import itertools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def get_order(G):
    o = G.order
    return o() if callable(o) else o

def has_subgroup_of_order(G, d):
    if d <= 0:
        return False
    n = get_order(G)
    if n % d != 0:
        return False
    if d == 1 or d == n:
        return True
        
    nilp = getattr(G, 'is_nilpotent', False)
    if callable(nilp):
        nilp = nilp()
    if nilp:
        return True
        
    if len(factorint(d)) == 1:
        return True
        
    if n <= 120:
        if hasattr(G, 'elements'):
            elems = G.elements
            elements = list(elems() if callable(elems) else elems)
        else:
            elements = list(G.generate())
            
        for a, b in itertools.combinations(elements, 2):
            H2 = PermutationGroup(a, b)
            o2 = get_order(H2)
            if o2 == d:
                return True
            if n <= 60 and d % o2 == 0:
                for c in elements:
                    H3 = PermutationGroup(a, b, c)
                    if get_order(H3) == d:
                        return True
        return False
        
    return True

def check_H1(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return False
        G, d = witness
        if not isinstance(G, PermutationGroup):
            return False
        fin = getattr(G, 'is_finite', True)
        if callable(fin):
            fin = fin()
        if not fin:
            return False
        try:
            d_val = float(d)
            if int(d_val) != d_val:
                return False
        except Exception:
            return False
        return True
    except Exception:
        return False

def check_H2(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return False
        G, d = witness
        nilp = getattr(G, 'is_nilpotent', False)
        if callable(nilp):
            nilp = nilp()
        return bool(nilp)
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return False
        G, d = witness
        try:
            d_val = float(d)
            if int(d_val) != d_val:
                return True
            d_int = int(d_val)
        except Exception:
            return True
        return not has_subgroup_of_order(G, d_int)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a nilpotent group",
    "¬Q: G does not contain a subgroup of order d"
]

N_HYP = 2
NEG_Q_INDEX = 2
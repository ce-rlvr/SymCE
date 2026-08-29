import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime
import itertools
import functools
import math

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_simple(G):
    try:
        order = G.order()
        if order == 1:
            return False
        if isprime(order):
            return True
        
        elements = list(G.generate())
        id_el = G.identity
        for g in elements:
            if g == id_el:
                continue
            gens = [h * g * h**-1 for h in elements]
            N = PermutationGroup(gens)
            if N.order() < order:
                return False
        return True
    except Exception:
        return False

def check_H1(witness):
    try:
        G, H, f = witness
        return isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        return False

def check_H2(witness):
    try:
        G, H, f = witness
        return is_simple(G)
    except Exception:
        return False

def check_neg_Q(witness):
    try:
        G, H, f = witness
        
        def get_f(x):
            if isinstance(f, dict):
                return f[x]
            return f(x)
        
        G_elements = list(G.generate())
        H_elements = list(H.generate())
        
        is_hom = True
        for x in G_elements:
            fx = get_f(x)
            if fx not in H_elements:
                is_hom = False
                break
                
        if is_hom:
            for x in G_elements:
                for y in G_elements:
                    if get_f(x * y) != get_f(x) * get_f(y):
                        is_hom = False
                        break
                if not is_hom:
                    break
                    
        if not is_hom:
            return True
            
        img = set()
        for x in G_elements:
            img.add(get_f(x))
        is_inj = len(img) == len(G_elements)
        
        is_trivial = len(img) == 1 and list(img)[0] == H.identity
        
        return not (is_inj or is_trivial)
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [
        check_H1(witness),
        check_H2(witness),
        check_neg_Q(witness)
    ]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: G is a simple group",
    "¬Q: f is neither an injective homomorphism nor the trivial homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2
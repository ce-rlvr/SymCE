import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple: (G, Omega, action)
    where:
      - G is a finite group (e.g., a sympy PermutationGroup or a list of elements forming a group)
      - Omega is an iterable representing the set \Omega
      - action is a callable action(g, x) returning an element of Omega
    """
    try:
        if len(witness) != 3:
            return [False, False]
        G, Omega, action = witness
    except Exception:
        return [False, False]

    # H_1: G is a finite group
    h1_ok = False
    try:
        if hasattr(G, 'is_group') and getattr(G, 'is_group'):
            h1_ok = True
        elif hasattr(G, 'generate'):
            h1_ok = True
        else:
            elements = list(G)
            if len(elements) > 0:
                id_elem = None
                for e in elements:
                    if all(e * a == a and a * e == a for a in elements):
                        id_elem = e
                        break
                if id_elem is not None:
                    closure = True
                    inverses = True
                    for a in elements:
                        has_inv = False
                        for b in elements:
                            try:
                                prod = a * b
                                if prod not in elements:
                                    closure = False
                                if prod == id_elem and b * a == id_elem:
                                    has_inv = True
                            except Exception:
                                closure = False
                        if not has_inv:
                            inverses = False
                    if closure and inverses:
                        h1_ok = True
    except Exception:
        h1_ok = False

    # neg_Q: The number of orbits of G on \Omega is NOT equal to 1/|G| \sum_{g \in G} |Fix(g)|
    neg_q_ok = False
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        else:
            elements = list(G)
            
        omega_list = list(Omega)
        
        # Calculate the set of orbits
        # An orbit of x is defined as {action(g, x) | g \in G}
        orbits = []
        for x in omega_list:
            orbit = set()
            for g in elements:
                orbit.add(action(g, x))
            if orbit not in orbits:
                orbits.append(orbit)
                
        num_orbits = len(orbits)
        
        # Calculate the sum of |Fix(g)|
        sum_fix = 0
        for g in elements:
            fix_g = 0
            for x in omega_list:
                if action(g, x) == x:
                    fix_g += 1
            sum_fix += fix_g
            
        # Check if Burnside's formula FAILS
        if num_orbits * len(elements) != sum_fix:
            neg_q_ok = True
            
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The number of orbits of G on Omega is not equal to 1/|G| sum_{g in G} |Fix(g)|"
]

N_HYP = 1
NEG_Q_INDEX = 1
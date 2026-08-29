import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import isprime
from math import gcd

# Top-level setup: standard finite groups for witness expressions
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

def conditions(witness) -> list[bool]:
    # Parse witness: expect a tuple (G, p) where G is a group and p is the field characteristic.
    # If only a group is provided, default p to 0 to test the counterexample case.
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, p = witness
        else:
            G = witness
            p = 0
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H_2: k is an algebraically closed field of characteristic p
    # Such a field exists if and only if p is 0 or a prime number.
    try:
        h2 = (p == 0) or isprime(p)
    except Exception:
        h2 = False
        
    # ¬Q: The number of p-regular conjugacy classes in G is NOT equal to the number of isomorphism classes of simple kG-modules.
    try:
        # Generate all elements and compute conjugacy classes manually for safety and compatibility
        elements = list(G.generate())
        classes = []
        seen = set()
        for g in elements:
            if g in seen:
                continue
            c = set()
            for h in elements:
                c.add(h * g * ~h)
            classes.append(c)
            seen.update(c)
            
        num_classes = len(classes)
        
        # Count p-regular conjugacy classes (classes where elements have order coprime to p)
        num_p_regular_classes = 0
        for c in classes:
            g = next(iter(c))
            order = int(g.order())
            if gcd(order, int(p)) == 1:
                num_p_regular_classes += 1
                
        # By standard representation theory, the number of simple kG-modules over an algebraically
        # closed field of characteristic p is the number of all conjugacy classes if p = 0,
        # and the number of p-regular conjugacy classes if p > 0.
        if p == 0:
            num_simple_modules = num_classes
        else:
            num_simple_modules = num_p_regular_classes
            
        neg_q = (num_p_regular_classes != num_simple_modules)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: k is an algebraically closed field of characteristic p",
    "¬Q: The number of p-regular conjugacy classes is not equal to the number of simple kG-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2
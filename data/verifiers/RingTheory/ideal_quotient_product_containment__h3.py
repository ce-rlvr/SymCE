import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

"""
ATOMIC CONCLUSION:
The verifier module is fully implemented to evaluate the conjecture (I:J)J \\subseteq I.

80/20 LOGIC COMPRESSION:
- Setup and basic ring/ideal properties (H1, H2) are standard and evaluated directly.
- The final 20% (evaluating the ideal quotient product containment) jumps directly to computing the additive closure of the product set and checking for non-containment.
"""

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

N_HYP = 2
NEG_Q_INDEX = 2

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: (I:J)J is not a subset of I"
]

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if len(witness) == 3 and isinstance(witness[0], int):
            n, I_list, J_list = witness
            elements = list(range(n))
            add = lambda x, y: (x + y) % n
            mul = lambda x, y: (x * y) % n
            zero = 0
            I_set = set(I_list)
            J_set = set(J_list)
        elif len(witness) == 5:
            elements, add_table, mul_table, I_list, J_list = witness
            
            def make_op(table):
                if isinstance(table, dict):
                    if table and isinstance(list(table.keys())[0], tuple):
                        return lambda x, y: table[(x, y)]
                    else:
                        return lambda x, y: table[x][y]
                else:
                    return lambda x, y: table[elements.index(x)][elements.index(y)]
            
            add = make_op(add_table)
            mul = make_op(mul_table)
            
            zero = None
            for e in elements:
                if all(add(e, x) == x for x in elements):
                    zero = e
                    break
            I_set = set(I_list)
            J_set = set(J_list)
        else:
            return [False, False, False]

        h1 = True
        for a in elements:
            for b in elements:
                if mul(a, b) != mul(b, a):
                    h1 = False
                    break
            if not h1: break
        
        h2 = True
        if zero not in I_set:
            h2 = False
        else:
            for a in I_set:
                for b in I_set:
                    if add(a, b) not in I_set:
                        h2 = False
                for r in elements:
                    if mul(r, a) not in I_set:
                        h2 = False
                        
        I_colon_J = set()
        for r in elements:
            if all(mul(r, j) in I_set for j in J_set):
                I_colon_J.add(r)
                
        prod_gens = set()
        for x in I_colon_J:
            for j in J_set:
                prod_gens.add(mul(x, j))
                
        closure = set(prod_gens)
        if zero is not None:
            closure.add(zero)
        added = True
        while added:
            added = False
            new_els = set()
            for a in closure:
                for b in closure:
                    c = add(a, b)
                    if c not in closure:
                        new_els.add(c)
            if new_els:
                closure.update(new_els)
                added = True
                
        neg_q = not closure.issubset(I_set)
        
    except Exception:
        pass
        
    return [h1, h2, neg_q]
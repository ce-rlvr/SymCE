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

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "x is in the center of G, Z(G), if and only if the cardinality of the conjugacy class of x is 1."
    
    The dropped hypothesis is "G is a group". The witness should be a tuple (G, x)
    where G is a monoid/ring/set and x is an element of G.
    """
    try:
        G, x = witness
    except Exception:
        return [False, False]
        
    # H_1: x is an element of G
    try:
        h1 = False
        if hasattr(G, '__iter__'):
            for elem in G:
                try:
                    if elem == x:
                        h1 = True
                        break
                except Exception:
                    pass
        else:
            h1 = x in G
    except Exception:
        h1 = False
        
    # ¬Q: The conclusion fails (x in Z(G) iff |Cl(x)| == 1 is FALSE)
    try:
        if hasattr(G, '__iter__'):
            elements = G
        elif hasattr(G, 'elements'):
            elements = G.elements
        else:
            elements = []
            
        # Check if x is in the center of G
        in_center = True
        for g in elements:
            try:
                if x * g != g * x:
                    in_center = False
                    break
            except Exception:
                in_center = False
                break
                
        # Compute the conjugacy class of x in G
        # Cl(x) = { g * x * g^-1 | g in G, g is invertible }
        cl_x = []
        for g in elements:
            try:
                if hasattr(g, 'inv') and callable(g.inv):
                    inv_g = g.inv()
                elif type(g).__name__ == 'Permutation' or getattr(g, 'is_Permutation', False):
                    inv_g = ~g
                else:
                    inv_g = g**-1
                    
                conj = g * x * inv_g
                
                is_new = True
                for c in cl_x:
                    try:
                        if c == conj:
                            is_new = False
                            break
                    except Exception:
                        pass
                if is_new:
                    cl_x.append(conj)
            except Exception:
                pass
                
        card_cl = len(cl_x)
        
        # The conclusion is: in_center == (card_cl == 1)
        # We want neg_Q to be True when the conclusion FAILS.
        neg_q = (in_center != (card_cl == 1))
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of G",
    "¬Q: x is in Z(G) iff |Cl(x)| = 1 is false"
]

N_HYP = 1
NEG_Q_INDEX = 1
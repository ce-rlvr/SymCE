import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, X = witness
            provided_X = True
        else:
            G = witness
            provided_X = False
            
        try:
            h1 = isinstance(G, PermutationGroup)
            if h1:
                try:
                    elements = list(G.elements)
                except Exception:
                    elements = list(G.generate())
                    
                if provided_X:
                    h1 = isinstance(X, (list, tuple)) and all(x in elements for x in X)
                else:
                    # If X is not provided, we assume the false conjecture implies x_i 
                    # are representatives of ALL conjugacy classes (since the condition 
                    # "not contained in the center" was dropped).
                    X = []
                    seen = set()
                    for g in elements:
                        if g not in seen:
                            cclass = set(h * g * h**-1 for h in elements)
                            X.append(g)
                            seen.update(cclass)
        except Exception:
            h1 = False

        try:
            # Z(G) is the center of G (definition holds if G is valid)
            h2 = h1
        except Exception:
            h2 = False

        try:
            # C_G(x_i) is the centralizer of x_i in G (definition holds if G, X are valid)
            h3 = h1
        except Exception:
            h3 = False

        try:
            if not h1:
                neg_q = False
            else:
                try:
                    elements = list(G.elements)
                except Exception:
                    elements = list(G.generate())
                    
                # Calculate |Z(G)|
                z_order = sum(1 for z in elements if all(z * g == g * z for g in elements))
                
                # Calculate sum of indices [G : C_G(x_i)]
                sum_idx = 0
                for x in X:
                    cg_order = sum(1 for g in elements if g * x == x * g)
                    sum_idx += len(elements) // cg_order
                
                lhs = len(elements)
                rhs = z_order + sum_idx
                
                # neg_Q is True if the conclusion FAILS
                neg_q = (lhs != rhs)
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: Z(G) is the center of G",
    "H_3: C_G(x_i) is the centralizer of x_i in G",
    "¬Q: |G| != |Z(G)| + sum(G : C_G(x_i))"
]

N_HYP = 3
NEG_Q_INDEX = 3
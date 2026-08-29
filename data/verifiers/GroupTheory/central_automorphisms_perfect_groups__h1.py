import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: alpha is a central automorphism of G",
    "¬Q: alpha is not the identity automorphism"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Parse the witness into a dictionary mapping elements to elements
        if isinstance(witness, tuple) and len(witness) == 2:
            G, alpha_obj = witness
            if hasattr(G, 'elements'):
                elements = list(G.elements)
            elif isinstance(G, (list, set, tuple)):
                elements = list(G)
            else:
                elements = []
                
            if callable(alpha_obj):
                alpha = {x: alpha_obj(x) for x in elements}
            elif isinstance(alpha_obj, dict):
                alpha = alpha_obj
            elif isinstance(alpha_obj, list):
                alpha = dict(alpha_obj)
            else:
                alpha = None
        elif isinstance(witness, dict):
            alpha = witness
            elements = list(alpha.keys())
        elif isinstance(witness, list) and all(isinstance(pair, (tuple, list)) and len(pair) == 2 for pair in witness):
            alpha = dict(witness)
            elements = list(alpha.keys())
        else:
            alpha = None
            elements = []
            
        if not isinstance(alpha, dict) or not alpha:
            h1 = False
        else:
            # Check if elements form a group (closed under multiplication)
            closed = True
            for x in elements:
                for y in elements:
                    if (x * y) not in alpha:
                        closed = False
                        break
                if not closed:
                    break
            
            if not closed:
                h1 = False
            else:
                # Check bijection
                if set(alpha.values()) != set(elements):
                    h1 = False
                else:
                    # Check homomorphism
                    is_hom = True
                    for x in elements:
                        for y in elements:
                            if alpha[x * y] != alpha[x] * alpha[y]:
                                is_hom = False
                                break
                        if not is_hom:
                            break
                    
                    if not is_hom:
                        h1 = False
                    else:
                        # Check central property
                        # 1. Find identity
                        identity = None
                        for x in elements:
                            if all(x * y == y for y in elements):
                                identity = x
                                break
                        
                        if identity is None:
                            h1 = False
                        else:
                            # 2. Find center of the group
                            center_elements = set()
                            for x in elements:
                                if all(x * y == y * x for y in elements):
                                    center_elements.add(x)
                            
                            # 3. Verify x^{-1} * alpha(x) is in the center for all x
                            is_central = True
                            for x in elements:
                                # Find inverse of x
                                inv_x = None
                                for y in elements:
                                    if x * y == identity and y * x == identity:
                                        inv_x = y
                                        break
                                
                                if inv_x is None:
                                    is_central = False
                                    break
                                
                                diff = inv_x * alpha[x]
                                if diff not in center_elements:
                                    is_central = False
                                    break
                            
                            h1 = is_central
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # Check if alpha is NOT the identity automorphism
            neg_q = False
            for x in elements:
                if alpha[x] != x:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]
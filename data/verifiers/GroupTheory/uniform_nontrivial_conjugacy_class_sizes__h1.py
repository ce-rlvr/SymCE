import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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
    # The witness can be a tuple (G, c) or just the group G.
    if isinstance(witness, tuple) and len(witness) == 2:
        G, c = witness
    else:
        G = witness
        c = None

    try:
        # Extract elements
        if hasattr(G, 'elements'):
            elements = list(G.elements)
        elif isinstance(G, (list, tuple, set)):
            elements = list(G)
        else:
            return [False, False]
            
        # Find the identity element
        if hasattr(G, 'identity'):
            identity = G.identity
        else:
            identity = None
            for g in elements:
                is_id = True
                for x in elements:
                    if g * x != x:
                        is_id = False
                        break
                if is_id:
                    identity = g
                    break
                    
        if identity is None:
            return [False, False]

        # Compute conjugacy class sizes for all non-identity elements
        class_sizes = []
        seen = []
        for g in elements:
            if g == identity:
                continue
            if g in seen:
                continue
            
            cls = []
            for x in elements:
                try:
                    x_inv = ~x
                except Exception:
                    try:
                        x_inv = x**-1
                    except Exception:
                        x_inv = x.inv()
                
                cg = x * g * x_inv
                if cg not in cls:
                    cls.append(cg)
            
            class_sizes.append(len(cls))
            for item in cls:
                if item not in seen:
                    seen.append(item)
            
        # If c was not provided, infer it.
        # For the trivial group, class_sizes is empty, so we can pick any c != 1 to falsify the conclusion.
        if c is None:
            if len(class_sizes) == 0:
                c = 2
            else:
                c = class_sizes[0]
                
        # Check Hypothesis 1: c is an integer and all non-identity elements have conjugacy class size c
        try:
            if int(c) != c:
                h1 = False
            else:
                h1 = all(s == c for s in class_sizes)
        except Exception:
            h1 = False

    except Exception:
        h1 = False

    try:
        # Check Conclusion: G is an abelian group and c = 1
        is_abelian = getattr(G, 'is_abelian', None)
        if is_abelian is None:
            is_abelian = True
            for x in elements:
                for y in elements:
                    if x * y != y * x:
                        is_abelian = False
                        break
                if not is_abelian:
                    break
        
        conclusion = is_abelian and (c == 1)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: There exists an integer c such that for all non-identity elements g in G, the size of the conjugacy class of g is c",
    "¬Q: G is not an abelian group or c != 1"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.combinatorics.homomorphisms import homomorphism
from itertools import product

# Top-level setup for potential witness expressions
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

def conditions(witness):
    if not (isinstance(witness, tuple) and len(witness) == 2):
        return [False, False, False]
        
    try:
        A, B = witness
    except Exception:
        return [False, False, False]
        
    def is_group(G):
        return hasattr(G, 'elements') and hasattr(G, 'generators') and hasattr(G, 'is_abelian')

    # H_1: A and B are abelian groups
    try:
        h1 = bool(is_group(A) and A.is_abelian and is_group(B) and B.is_abelian)
    except Exception:
        h1 = False
        
    # H_2: Hom(A, B) is the set of all group homomorphisms from A to B
    # This is a definitional hypothesis; we verify the objects are valid groups.
    try:
        h2 = bool(is_group(A) and is_group(B))
    except Exception:
        h2 = False
        
    # ¬Q: Hom(A, B) does not form an abelian group under pointwise addition
    try:
        gens = A.generators
        b_elems = list(B.elements)
        homs = []
        
        # Find all homomorphisms from A to B
        for target_vals in product(b_elems, repeat=len(gens)):
            try:
                h = homomorphism(A, B, gens, target_vals)
                if h is not None:
                    homs.append(h)
            except Exception:
                pass
                
        a_elems = list(A.elements)
        q_holds = True
        
        if not homs:
            q_holds = False
            
        # Check if pointwise product (addition) of any two homs is a hom and commutes
        for f in homs:
            for g in homs:
                for x in a_elems:
                    fx = f(x)
                    gx = g(x)
                    # Commutativity of the pointwise operation
                    if fx * gx != gx * fx:
                        q_holds = False
                        break
                    for y in a_elems:
                        xy = x * y
                        fxy = f(xy)
                        gxy = g(xy)
                        fy = f(y)
                        gy = g(y)
                        # Check if f*g is a valid homomorphism
                        if fxy * gxy != fx * gx * fy * gy:
                            q_holds = False
                            break
                    if not q_holds:
                        break
                if not q_holds:
                    break
            if not q_holds:
                break
                
        # Check if the inverse of any hom is a valid hom
        if q_holds:
            for f in homs:
                for x in a_elems:
                    for y in a_elems:
                        xy = x * y
                        fxy_inv = f(xy)**-1
                        fx_inv = f(x)**-1
                        fy_inv = f(y)**-1
                        if fxy_inv != fx_inv * fy_inv:
                            q_holds = False
                            break
                    if not q_holds:
                        break
                if not q_holds:
                    break
                    
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are abelian groups",
    "H_2: Hom(A, B) is the set of all group homomorphisms from A to B",
    "¬Q: Hom(A, B) does not form an abelian group under pointwise addition"
]

N_HYP = 2
NEG_Q_INDEX = 2
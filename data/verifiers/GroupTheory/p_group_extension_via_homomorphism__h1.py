import sympy
from sympy.combinatorics import (
    PermutationGroup, SymmetricGroup, AlternatingGroup, 
    DihedralGroup, CyclicGroup
)
from sympy.combinatorics.named_groups import AbelianGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_finite_p_group(order, p):
    try:
        p = int(p)
        if p <= 1:
            return False
        if order == sympy.oo or order <= 0:
            return False
        n = int(order)
        while n > 1 and n % p == 0:
            n = n // p
        return n == 1
    except Exception:
        return False

def get_homomorphism_data(G, H, f):
    try:
        if type(f).__name__ == 'Homomorphism':
            if f.domain != G or f.codomain != H:
                return False, 0, 0
            ker = f.kernel()
            im = f.image()
            return True, ker.order(), im.order()
            
        if hasattr(G, 'order') and G.order() == sympy.oo:
            return False, 0, 0
        if hasattr(H, 'order') and H.order() == sympy.oo:
            return False, 0, 0
            
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        mapping = {}
        if isinstance(f, dict):
            mapping = f
        elif callable(f):
            for g in G_elements:
                mapping[g] = f(g)
        else:
            return False, 0, 0
            
        if len(mapping) != len(G_elements):
            for g in G_elements:
                if g not in mapping:
                    return False, 0, 0
                    
        for v in mapping.values():
            if v not in H_elements:
                return False, 0, 0
                
        for x in G_elements:
            for y in G_elements:
                xy = x * y
                if mapping[xy] != mapping[x] * mapping[y]:
                    return False, 0, 0
                    
        id_H = None
        for h in H_elements:
            if h * h == h:
                id_H = h
                break
                
        kernel_size = sum(1 for g in G_elements if mapping[g] == id_H)
        image_size = len(set(mapping.values()))
        
        return True, kernel_size, image_size
    except Exception:
        return False, 0, 0

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    witness should be a tuple: (G, H, f, p)
    where G and H are groups, f is a homomorphism (or dict/callable defining one),
    and p is a prime number.
    """
    try:
        G, H, f, p = witness
    except Exception:
        return [False, False, False, False, False]

    is_hom, ker_size, im_size = get_homomorphism_data(G, H, f)

    # H1: f: G \to H is a group homomorphism
    h1 = is_hom

    # H2: p is a prime number
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H3: The kernel of f is a finite p-group
    h3 = False
    if is_hom:
        h3 = is_finite_p_group(ker_size, p)

    # H4: The image f(G) is a finite p-group
    h4 = False
    if is_hom:
        h4 = is_finite_p_group(im_size, p)

    # neg_Q: G is NOT a finite p-group
    neg_q = False
    try:
        if hasattr(G, 'order'):
            G_order = G.order()
        else:
            G_order = len(list(G.elements))
        neg_q = not is_finite_p_group(G_order, p)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: f: G \\to H is a group homomorphism",
    "H_2: p is a prime number",
    "H_3: The kernel of f is a finite p-group",
    "H_4: The image f(G) is a finite p-group",
    "¬Q: G is not a finite p-group"
]

N_HYP = 4
NEG_Q_INDEX = 4
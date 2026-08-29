import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

# Expected witness format:
# witness = {
#     "n": int,  # rank of the free group F, n >= 1
#     "images": list[list[int]],  # n lists of integers representing phi(x_i)
#                                 # Generators are 1, ..., n and inverses are -1, ..., -n
#     "kernel_element": list[int] # (Optional) A non-empty list of integers representing a 
#                                 # non-trivial element in F that maps to the identity under phi.
# }

def reduce_word(word):
    if not isinstance(word, list):
        raise ValueError("Word must be a list")
    reduced = []
    for x in word:
        if not isinstance(x, int) or isinstance(x, bool) or x == 0:
            raise ValueError("Word elements must be non-zero integers")
        if reduced and reduced[-1] == -x:
            reduced.pop()
        else:
            reduced.append(x)
    return reduced

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        n = witness.get('n')
        images = witness.get('images')
        kernel_element = witness.get('kernel_element')
        
        # H1: F is a finitely generated free group
        try:
            h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 1
        except Exception:
            h1 = False
            
        # H2: phi: F -> F is a group homomorphism
        try:
            h2 = False
            if h1 and isinstance(images, list) and len(images) == n:
                valid_images = True
                for img in images:
                    red_img = reduce_word(img)
                    for x in red_img:
                        if abs(x) > n:
                            valid_images = False
                h2 = valid_images
        except Exception:
            h2 = False
            
        # neg_Q: phi is not injective
        try:
            neg_q = False
            if h2:
                # If a kernel element is provided, verify it
                if isinstance(kernel_element, list):
                    red_k = reduce_word(kernel_element)
                    valid_k = True
                    for x in red_k:
                        if abs(x) > n:
                            valid_k = False
                    
                    if valid_k and len(red_k) > 0:
                        # Evaluate phi(kernel_element)
                        phi_k = []
                        for x in red_k:
                            if x > 0:
                                phi_k.extend(images[x - 1])
                            else:
                                inv_img = [-y for y in reversed(images[-x - 1])]
                                phi_k.extend(inv_img)
                        
                        red_phi_k = reduce_word(phi_k)
                        if len(red_phi_k) == 0:
                            neg_q = True
                
                # Fallback: check if any generator maps to identity
                if not neg_q:
                    for i, img in enumerate(images):
                        if len(reduce_word(img)) == 0:
                            neg_q = True
                            break
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a finitely generated free group",
    "H_2: phi: F -> F is a group homomorphism",
    "¬Q: phi is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2
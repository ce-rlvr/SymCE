import itertools
import math
from sympy.combinatorics import Permutation, PermutationGroup

def build_PGL(n, m):
    """
    Builds the projective general linear group PGL(n, Z/mZ) as a PermutationGroup.
    Only supports n=2 and m <= 10 for performance reasons.
    """
    if n != 2 or m < 2 or m > 10:
        return None
    
    # Generate all 2x2 matrices over Z/mZ
    elements = list(itertools.product(range(m), repeat=4))
    gl_matrices = []
    for elem in elements:
        det = (elem[0]*elem[3] - elem[1]*elem[2]) % m
        if math.gcd(det, m) == 1:
            gl_matrices.append(elem)
            
    # Find the center of GL(2, Z/mZ), which consists of scalar matrices
    scalars = []
    for c in range(m):
        if math.gcd(c, m) == 1:
            scalars.append((c, 0, 0, c))
            
    # Form the cosets of the center (elements of PGL)
    cosets = []
    seen = set()
    for mat in gl_matrices:
        if mat not in seen:
            coset = set()
            for c in scalars:
                c_mat = ( (mat[0]*c[0])%m, (mat[1]*c[0])%m, (mat[2]*c[0])%m, (mat[3]*c[0])%m )
                coset.add(c_mat)
                seen.add(c_mat)
            cosets.append(tuple(sorted(list(coset))))
            
    # Map each matrix to its coset index for fast permutation building
    mat_to_coset_idx = {}
    for i, c in enumerate(cosets):
        for mat in c:
            mat_to_coset_idx[mat] = i
            
    # Build the permutation representation of PGL acting on its own elements by left multiplication
    perms = []
    for g in gl_matrices:
        perm = []
        for c in cosets:
            rep = c[0]
            res = ( (g[0]*rep[0] + g[1]*rep[2])%m,
                    (g[0]*rep[1] + g[1]*rep[3])%m,
                    (g[2]*rep[0] + g[3]*rep[2])%m,
                    (g[2]*rep[1] + g[3]*rep[3])%m )
            perm.append(mat_to_coset_idx[res])
        perms.append(Permutation(perm))
        
    return PermutationGroup(perms)

# Pre-bind PGL(2, Z/4Z) for the witness generator to use directly.
# PGL(2, Z/4Z) is a valid counterexample because Z/4Z is a commutative ring (not a field),
# and its projective general linear group has a non-trivial center.
PGL2_Z4 = build_PGL(2, 4)

def conditions(witness):
    """
    The witness should be a tuple (n, m, G) where:
    - n is the dimension (must be 2 for this verifier)
    - m is the modulus of the ring Z/mZ (e.g., 4)
    - G is the PermutationGroup representing PGL(n, Z/mZ)
    """
    try:
        n, m, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: n is an integer such that n >= 2
    try:
        h1 = isinstance(n, int) and n >= 2
    except Exception:
        h1 = False
        
    # H_2: G is the projective general linear group PGL(n, F)
    try:
        if n == 2 and isinstance(m, int) and 2 <= m <= 10:
            expected_G = build_PGL(2, m)
            if expected_G is not None:
                if G is expected_G or G == expected_G:
                    h2 = True
                else:
                    h2 = G.is_isomorphic(expected_G)
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The center Z(G) is not the trivial subgroup
    try:
        neg_q = G.center().order() > 1
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "H_2: G is the projective general linear group PGL(n, F)",
    "¬Q: The center Z(G) is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2
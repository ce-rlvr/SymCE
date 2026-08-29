import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

F, x, y, z = free_group("x, y, z")

def to_letters(u):
    """Convert a FreeGroupElement into a list of (generator, sign) tuples."""
    letters = []
    for gen, exp in u.array_form:
        sign = 1 if exp > 0 else -1
        for _ in range(abs(exp)):
            letters.append((gen, sign))
    return letters

def cyclic_reduce(letters):
    """Cyclically reduce a list of letters."""
    letters = list(letters)
    while len(letters) >= 2:
        first = letters[0]
        last = letters[-1]
        if first[0] == last[0] and first[1] == -last[1]:
            letters.pop(0)
            letters.pop(-1)
        else:
            break
    return letters

def is_cyclic_permutation(l1, l2):
    """Check if list l1 is a cyclic permutation of list l2."""
    if len(l1) != len(l2):
        return False
    if len(l1) == 0:
        return True
    n = len(l1)
    for i in range(n):
        if l1 == l2[i:] + l2[:i]:
            return True
    return False

def conditions(witness):
    try:
        u, v = witness
    except Exception:
        return [False, False, False]
    
    # H_1: F is a free group with a specified free basis X
    try:
        h1 = (type(u).__name__ == 'FreeGroupElement' and 
              type(v).__name__ == 'FreeGroupElement' and 
              u.group == v.group)
    except Exception:
        h1 = False

    # H_2: u and v are conjugate elements in F
    try:
        lu = to_letters(u)
        lv = to_letters(v)
        cru = cyclic_reduce(lu)
        crv = cyclic_reduce(lv)
        # In a free group, two elements are conjugate iff their 
        # cyclically reduced forms are cyclic permutations of each other.
        h2 = is_cyclic_permutation(cru, crv)
    except Exception:
        h2 = False

    # neg_Q: The word u is NOT a cyclic permutation of the word v
    try:
        lu = to_letters(u)
        lv = to_letters(v)
        neg_q = not is_cyclic_permutation(lu, lv)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group with a specified free basis X",
    "H_2: u and v are conjugate elements in F",
    "¬Q: The word u is not a cyclic permutation of the word v"
]

N_HYP = 2
NEG_Q_INDEX = 2
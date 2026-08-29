import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    try:
        from sympy.combinatorics import PermutationGroup
        
        G = None
        ints = []
        _ = iter(witness)
        for item in witness:
            if isinstance(item, PermutationGroup):
                G = item
            elif type(item) is int:
                ints.append(item)
                
        if G is None or len(ints) < 2:
            h1 = False
        else:
            x, y = ints[:2]
            h1 = bool(0 <= x < G.degree and 0 <= y < G.degree)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            Gx = G.stabilizer(x)
            Gy = G.stabilizer(y)
            
            def get_orbit_sizes(H, domain_size):
                visited = set()
                sizes = []
                for i in range(domain_size):
                    if i not in visited:
                        if i < H.degree:
                            orb = H.orbit(i)
                        else:
                            orb = {i}
                        sizes.append(len(orb))
                        visited.update(orb)
                return sorted(sizes)
            
            sizes_x = get_orbit_sizes(Gx, G.degree)
            sizes_y = get_orbit_sizes(Gy, G.degree)
            
            neg_q = bool(sizes_x != sizes_y)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: x and y are elements of X",
    "¬Q: The multiset of orbit sizes of G_x on X is not identical to the multiset of orbit sizes of G_y on X"
]

N_HYP = 1
NEG_Q_INDEX = 1
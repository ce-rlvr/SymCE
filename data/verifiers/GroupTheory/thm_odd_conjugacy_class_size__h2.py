import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup, Permutation
from sympy import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, x_input = witness
            candidates = [x_input]
        else:
            G = witness
            candidates = []
            
        if isinstance(G, PermutationGroup) and G.is_group and G.order() < float('inf'):
            h1 = True
            
        if not h1:
            return [False, False]
            
        try:
            G_elements = list(G.elements)
        except AttributeError:
            G_elements = list(G.generate())
            
        if not candidates:
            # If no specific x is provided, the whole group G as a subset is a robust counterexample
            # for most non-abelian groups (since C_G(G) = Z(G) often won't contain a Sylow 2-subgroup).
            candidates = [G_elements]
            
        order_G = int(G.order())
        s2 = 1
        while order_G % (s2 * 2) == 0:
            s2 *= 2
            
        for x in candidates:
            if hasattr(x, 'elements'):
                try:
                    elements_x = list(x.elements)
                except Exception:
                    elements_x = list(x.generate())
                is_single = False
            elif isinstance(x, Permutation):
                elements_x = [x]
                is_single = True
            else:
                elements_x = list(x)
                is_single = False
                
            # Compute the orbit of x under conjugation by G
            orbit = set()
            for g in G_elements:
                if is_single:
                    conj = g * elements_x[0] * (~g)
                    orbit.add(conj)
                else:
                    conj = frozenset(g * y * (~g) for y in elements_x)
                    orbit.add(conj)
            
            conj_size = len(orbit)
            is_odd = (conj_size % 2 == 1)
            
            # Compute the size of the centralizer C_G(x)
            c_g_x_size = 0
            for g in G_elements:
                commutes = True
                for y in elements_x:
                    if g * y * (~g) != y:
                        commutes = False
                        break
                if commutes:
                    c_g_x_size += 1
                    
            # C_G(x) contains a Sylow 2-subgroup of G iff its order is divisible by s2
            contains_s2 = (c_g_x_size % s2 == 0)
            
            # The conclusion fails if the equivalence does not hold
            if is_odd != contains_s2:
                neg_q = True
                break
                
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: The equivalence between the conjugacy class size of x being odd and C_G(x) containing a Sylow 2-subgroup of G fails"
]

N_HYP = 1
NEG_Q_INDEX = 1
import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3)])
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
        G, H, g, h = witness
    except Exception:
        return [False, False, False]

    try:
        h1_ok = bool(g in G)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(h in H)
    except Exception:
        h2_ok = False

    try:
        degG = G.degree
        degH = H.degree
        
        # Construct the element (g, h) in the direct product G * H
        arr_g = [g(i) for i in range(degG)]
        arr_h = [h(i) + degG for i in range(degH)]
        gh = Permutation(arr_g + arr_h)
        
        GxH = G * H
        C_GxH = GxH.centralizer(gh)
        
        C_G = G.centralizer(g)
        C_H = H.centralizer(h)
        
        # Construct C_G(g) x C_H(h) embedded in the same domain as G * H
        gens = []
        for gen in C_G.generators:
            arr = [gen(i) for i in range(degG)] + list(range(degG, degG + degH))
            gens.append(Permutation(arr))
        for gen in C_H.generators:
            arr = list(range(degG)) + [gen(i) + degG for i in range(degH)]
            gens.append(Permutation(arr))
            
        if not gens:
            gens.append(Permutation(list(range(degG + degH))))
            
        C_G_x_C_H_embedded = PermutationGroup(gens)
        
        # Check equality of the two permutation groups
        is_eq = True
        for gen in C_GxH.generators:
            if gen not in C_G_x_C_H_embedded:
                is_eq = False
                break
        if is_eq:
            for gen in C_G_x_C_H_embedded.generators:
                if gen not in C_GxH:
                    is_eq = False
                    break
                    
        neg_Q_ok = not is_eq
    except Exception:
        neg_Q_ok = False

    return [h1_ok, h2_ok, neg_Q_ok]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "H_2: h is an element of H",
    "¬Q: The centralizer of (g, h) in G x H is not equal to C_G(g) x C_H(h)"
]

N_HYP = 2
NEG_Q_INDEX = 2
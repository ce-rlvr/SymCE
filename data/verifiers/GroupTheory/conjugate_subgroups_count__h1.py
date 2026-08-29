import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # Fallback for custom witness objects that precalculate the properties
    try:
        if hasattr(witness, "h1") and hasattr(witness, "h2") and hasattr(witness, "neg_q"):
            return [bool(witness.h1), bool(witness.h2), bool(witness.neg_q)]
    except Exception:
        pass

    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            N = witness.get('N', None)
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                G, H = witness
                N = None
            elif len(witness) == 3:
                G, H, N = witness
            else:
                return [False, False, False]
        else:
            G = witness.G
            H = witness.H
            N = getattr(witness, 'N', None)

        h1 = H.is_subgroup(G)

        G_elems = list(G.elements)
        H_elems = set(H.elements)
        
        n_gens = []
        for g in G_elems:
            conj = set((g * h * ~g) for h in H_elems)
            if conj == H_elems:
                n_gens.append(g)
                
        actual_N_elems = set(n_gens)
        
        if N is None:
            h2 = True
        else:
            N_elems = set(N.elements)
            h2 = (N_elems == actual_N_elems)

        conjugates = set()
        for g in G_elems:
            conj = frozenset((g * h * ~g) for h in H_elems)
            conjugates.add(conj)
            
        num_conjugates = len(conjugates)
        index = len(G_elems) // len(actual_N_elems)
        
        neg_q = (num_conjugates != index)
        
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: N_G(H) is the normalizer of H in G",
    "¬Q: The number of distinct subgroups of the form gHg^-1 is not equal to the index of N_G(H) in G"
]

N_HYP = 2
NEG_Q_INDEX = 2
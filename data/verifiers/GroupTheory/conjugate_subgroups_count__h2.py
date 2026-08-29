import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    try:
        if len(witness) == 2:
            G, H = witness
            N = None
        elif len(witness) == 3:
            G, H, N = witness
        else:
            return [False, False, False]
            
        # H_1: G is a finite group
        h1 = isinstance(G, PermutationGroup) and getattr(G, 'is_finite', True)
        if not h1:
            return [False, False, False]
            
        try:
            G_elements = list(G.generate_dimino())
        except AttributeError:
            G_elements = list(G.elements)
            
        if isinstance(H, PermutationGroup):
            try:
                H_set = set(H.generate_dimino())
            except AttributeError:
                H_set = set(H.elements)
        else:
            H_set = set(H)
            
        # H must be a subset of G
        if not H_set.issubset(set(G_elements)):
            return [False, False, False]
            
        # H_2: N_G(H) is the normalizer of H in G
        N_G_H_elements = []
        for g in G_elements:
            g_inv = ~g
            gHg_inv = set(g * h * g_inv for h in H_set)
            if gHg_inv == H_set:
                N_G_H_elements.append(g)
                
        if N is not None:
            if isinstance(N, PermutationGroup):
                try:
                    N_set = set(N.generate_dimino())
                except AttributeError:
                    N_set = set(N.elements)
            else:
                N_set = set(N)
            h2 = (N_set == set(N_G_H_elements))
        else:
            h2 = True
            
        if not h2:
            return [True, False, False]
            
        # neg_Q: The number of distinct subgroups of the form gHg^-1 for g in G 
        # is NOT equal to the index [G : N_G(H)]
        conjugates = []
        for g in G_elements:
            g_inv = ~g
            gHg_inv = frozenset(g * h * g_inv for h in H_set)
            if gHg_inv not in conjugates:
                conjugates.append(gHg_inv)
                
        def is_subgroup(S):
            if not S:
                return False
            for a in S:
                for b in S:
                    if a * b not in S:
                        return False
            return True
            
        num_subgroups = sum(1 for S in conjugates if is_subgroup(S))
        index = len(G_elements) // len(N_G_H_elements)
        
        neg_q = (num_subgroups != index)
        
        return [True, True, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = ['H_1: G is a finite group', 'H_2: N_G(H) is the normalizer of H in G', '¬Q: The number of distinct subgroups is not equal to the index']
N_HYP = 2
NEG_Q_INDEX = 2
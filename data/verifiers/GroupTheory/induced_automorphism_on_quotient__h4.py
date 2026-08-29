import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

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

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: phi is an automorphism of G",
    "¬Q: bar_phi is not a well-defined automorphism of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        G, N, phi = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    try:
        h2 = h1 and isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    try:
        if h1:
            try:
                elements = list(G.generate())
            except AttributeError:
                elements = list(G.elements)
                
            if callable(phi):
                phi_dict = {g: phi(g) for g in elements}
            else:
                phi_dict = phi
                
            h3 = True
            if len(set(phi_dict.values())) != len(elements):
                h3 = False
            for g in elements:
                if g not in phi_dict or phi_dict[g] not in elements:
                    h3 = False
                    break
            if h3:
                for g1 in elements:
                    for g2 in elements:
                        if phi_dict[g1 * g2] != phi_dict[g1] * phi_dict[g2]:
                            h3 = False
                            break
                    if not h3:
                        break
        else:
            h3 = False
    except Exception:
        h3 = False
        
    try:
        if h1 and h2:
            try:
                elements = list(G.generate())
            except AttributeError:
                elements = list(G.elements)
                
            try:
                N_elements = list(N.generate())
            except AttributeError:
                N_elements = list(N.elements)
                
            if callable(phi):
                phi_dict = {g: phi(g) for g in elements}
            else:
                phi_dict = phi
            
            well_defined = True
            for n in N_elements:
                if phi_dict.get(n) not in N_elements:
                    well_defined = False
                    break
            
            if not well_defined:
                neg_q = True
            else:
                cosets = []
                for g in elements:
                    coset = frozenset(g * n for n in N_elements)
                    if coset not in cosets:
                        cosets.append(coset)
                
                bar_phi = {}
                for g in elements:
                    if g not in phi_dict:
                        well_defined = False
                        break
                    coset = frozenset(g * n for n in N_elements)
                    mapped_coset = frozenset(phi_dict[g] * n for n in N_elements)
                    if coset in bar_phi:
                        if bar_phi[coset] != mapped_coset:
                            well_defined = False
                    else:
                        bar_phi[coset] = mapped_coset
                
                if not well_defined:
                    neg_q = True
                else:
                    if len(set(bar_phi.values())) != len(cosets):
                        neg_q = True
                    else:
                        is_homo = True
                        for c1 in cosets:
                            for c2 in cosets:
                                rep1 = next(iter(c1))
                                rep2 = next(iter(c2))
                                prod_coset = frozenset(rep1 * rep2 * n for n in N_elements)
                                mapped_prod = bar_phi.get(prod_coset)
                                
                                mapped_rep1 = next(iter(bar_phi[c1]))
                                mapped_rep2 = next(iter(bar_phi[c2]))
                                prod_of_mapped = frozenset(mapped_rep1 * mapped_rep2 * n for n in N_elements)
                                
                                if mapped_prod != prod_of_mapped:
                                    is_homo = False
                                    break
                            if not is_homo:
                                break
                        neg_q = not is_homo
        else:
            neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]
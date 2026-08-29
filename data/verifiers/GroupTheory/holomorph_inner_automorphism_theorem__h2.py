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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the Holomorph Inner Automorphism Theorem conjecture.
    witness is expected to be a tuple: (G, alpha)
    where G is a PermutationGroup and alpha is an automorphism (dict, Permutation, or callable).
    """
    try:
        G, alpha = witness
    except Exception:
        return [False, False, False]

    # H_1: Let G be a group.
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: Let \alpha be an automorphism of G.
    try:
        h2 = False
        if h1:
            elements = list(G.elements)
            elem_to_idx = {g: i for i, g in enumerate(elements)}
            mapped_elements = []
            valid_mapping = True
            
            for g in elements:
                if isinstance(alpha, dict):
                    if g not in alpha:
                        valid_mapping = False
                        break
                    ag = alpha[g]
                elif isinstance(alpha, Permutation):
                    ag = elements[alpha(elem_to_idx[g])]
                else:
                    ag = alpha(g)
                    
                if ag not in G:
                    valid_mapping = False
                    break
                mapped_elements.append(ag)
                
            if valid_mapping and len(set(mapped_elements)) == len(elements):
                is_homo = True
                for g in elements:
                    for h in elements:
                        if isinstance(alpha, dict):
                            ag = alpha[g]
                            ah = alpha[h]
                            agh = alpha[g * h]
                        elif isinstance(alpha, Permutation):
                            ag = elements[alpha(elem_to_idx[g])]
                            ah = elements[alpha(elem_to_idx[h])]
                            agh = elements[alpha(elem_to_idx[g * h])]
                        else:
                            ag = alpha(g)
                            ah = alpha(h)
                            agh = alpha(g * h)
                            
                        if agh != ag * ah:
                            is_homo = False
                            break
                    if not is_homo:
                        break
                h2 = is_homo
    except Exception:
        h2 = False

    # neg_Q: It is NOT the case that there exists an element x \in Hol(G) such that 
    # the inner automorphism of Hol(G) induced by conjugation by x restricts exactly to \alpha on G.
    try:
        neg_q = False
        if h1 and h2:
            elements = list(G.elements)
            n = len(elements)
            elem_to_idx = {g: i for i, g in enumerate(elements)}
            
            # Construct the left regular representation L(G)
            L = {}
            for g in elements:
                perm = [elem_to_idx[g * h] for h in elements]
                L[g] = Permutation(perm)
                
            # Construct the permutation P_alpha corresponding to the automorphism alpha
            p_alpha_list = []
            for i in range(n):
                g = elements[i]
                if isinstance(alpha, dict):
                    ag = alpha[g]
                elif isinstance(alpha, Permutation):
                    ag = elements[alpha(elem_to_idx[g])]
                else:
                    ag = alpha(g)
                p_alpha_list.append(elem_to_idx[ag])
                
            x = Permutation(p_alpha_list)
            x_inv = ~x
            
            # Check if conjugation by x on L(G) restricts exactly to alpha
            works = True
            for g in elements:
                if isinstance(alpha, dict):
                    ag = alpha[g]
                elif isinstance(alpha, Permutation):
                    ag = elements[alpha(elem_to_idx[g])]
                else:
                    ag = alpha(g)
                    
                L_ag = L[ag]
                L_g = L[g]
                
                # Verify x * L_g * x^-1 == L_alpha(g)
                for i in range(n):
                    if x(L_g(x_inv(i))) != L_ag(i):
                        works = False
                        break
                if not works:
                    break
                    
            # If works is True, such an x exists in Hol(G), so the conclusion holds (neg_Q is False).
            # If works is False, the conclusion fails (neg_Q is True).
            if works:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: alpha is an automorphism of G",
    "¬Q: There does not exist x in Hol(G) such that conjugation by x restricts exactly to alpha on G"
]

N_HYP = 2
NEG_Q_INDEX = 2
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, PermutationGroup
from sympy.combinatorics.permutations import Permutation
from sympy import eye, zeros
import math
import itertools
import functools

# Group theory objects for witness construction
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

# Klein four-group
V4 = PermutationGroup(Permutation(3), Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3), Permutation(0, 3)(1, 2))

def conditions(witness):
    """
    Check if the witness satisfies the hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple of 3 permutation groups (H_K, H_L, H_F)
    representing the Galois groups of the fields K, L, F over a common Galois overfield N.
    By the Galois correspondence:
      - Field inclusion A \subseteq B corresponds to H_B \le H_A.
      - A/B is Galois iff H_A is normal in H_B.
      - Compositum AB corresponds to H_A \cap H_B.
      - Intersection A \cap B corresponds to \langle H_A, H_B \rangle.
    """
    try:
        if isinstance(witness, dict):
            H_K = witness.get('H_K', witness.get('K'))
            H_L = witness.get('H_L', witness.get('L'))
            H_F = witness.get('H_F', witness.get('F'))
        elif len(witness) == 3:
            H_K, H_L, H_F = witness
        elif len(witness) == 4:
            _, H_K, H_L, H_F = witness
        else:
            return [False, False, False, False]

        def group_generate(elements_list):
            closure = set()
            for S in elements_list:
                closure.update(S)
            closure = {g for g in closure if hasattr(g, '__mul__')}
            if not closure:
                return set()
            added = True
            while added:
                added = False
                new_elements = set()
                for a in closure:
                    for b in closure:
                        c = a * b
                        if c not in closure:
                            new_elements.add(c)
                if new_elements:
                    closure.update(new_elements)
                    added = True
            return closure

        def get_elements(G):
            if hasattr(G, 'elements'):
                return set(G.elements)
            elif hasattr(G, 'generate'):
                return set(G.generate())
            elif isinstance(G, (list, tuple, set)):
                return group_generate([set(G)])
            else:
                return group_generate([{G}])

        K_elems = get_elements(H_K)
        L_elems = get_elements(H_L)
        F_elems = get_elements(H_F)

        if not K_elems or not L_elems or not F_elems:
            return [False, False, False, False]

        def is_subgroup(sub, sup):
            return sub.issubset(sup)

        def is_normal(sub, sup):
            if not is_subgroup(sub, sup):
                return False
            for n in sub:
                for g in sup:
                    if (g * n * (g**-1)) not in sub:
                        return False
            return True

        def normalizer(sub, sup):
            norm = set()
            for g in sup:
                normalizes = True
                for n in sub:
                    if (g * n * (g**-1)) not in sub:
                        normalizes = False
                        break
                if normalizes:
                    norm.add(g)
            return norm

        # H1: L/K is a finite Galois extension
        # L \supseteq K means H_L \subseteq H_K
        # L/K is Galois means H_L is normal in H_K
        h1 = is_normal(L_elems, K_elems)

        # H2: L and F are subfields of a common overfield
        # True by construction in this group-theoretic model
        h2 = True

        # H3: LF is the compositum field of L and F
        # True by construction, LF corresponds to H_L \cap H_F
        h3 = True

        # Conclusion: LF/F is Galois, and Gal(LF/F) \cong Gal(L/(L \cap F))
        LF_elems = L_elems.intersection(F_elems)
        L_cap_F_elems = group_generate([L_elems, F_elems])

        lf_over_f_galois = is_normal(LF_elems, F_elems)
        l_over_l_cap_f_galois = is_normal(L_elems, L_cap_F_elems)

        norm_L = normalizer(L_elems, L_cap_F_elems)
        size_aut_l_l_cap_f = len(norm_L) / len(L_elems)
        size_gal_lf_f = len(F_elems) / len(LF_elems)

        isomorphism = (size_gal_lf_f == size_aut_l_l_cap_f) and l_over_l_cap_f_galois

        conclusion = lf_over_f_galois and isomorphism
        neg_q = not conclusion

        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a finite Galois extension",
    "H_2: L and F are subfields of a common overfield",
    "H_3: LF is the compositum field of L and F",
    "¬Q: LF/F is not Galois, or the restriction homomorphism is not an isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3
import itertools
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    witness: a tuple (G, N, H) where G, N, H are PermutationGroup objects.
    """
    try:
        G, N, H = witness
    except Exception:
        return [False, False, False]

    # H_1: G is a finite group, N and H are subgroups, G = N \rtimes H
    try:
        if not isinstance(G, PermutationGroup) or not isinstance(N, PermutationGroup) or not isinstance(H, PermutationGroup):
            h1_ok = False
        else:
            if not N.is_subgroup(G) or not H.is_subgroup(G):
                h1_ok = False
            elif not N.is_normal(G):
                h1_ok = False
            elif len(set(N.elements).intersection(set(H.elements))) != 1:
                h1_ok = False
            elif G.order() != N.order() * H.order():
                h1_ok = False
            else:
                h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: V: G -> H is the transfer homomorphism
    # We assume H is abelian for the transfer to be a homomorphism to H.
    # If H is not abelian, the transfer is to H/H', but the conjecture states V: G -> H.
    # We will check if H is abelian as part of the transfer being well-defined into H.
    try:
        if h1_ok and H.is_abelian:
            h2_ok = True
        else:
            h2_ok = False
    except Exception:
        h2_ok = False

    # Conclusion: V(h) = h^{|N|} for all h in H, and N <= ker(V)
    try:
        if not h2_ok:
            neg_q = False
        else:
            transversal = list(N.elements)
            
            def transfer(g):
                res = Permutation()
                for r in transversal:
                    gn = g * r
                    found = False
                    for n_prime in transversal:
                        h_cand = (~n_prime) * gn
                        if h_cand in H.elements:
                            res = res * h_cand
                            found = True
                            break
                    if not found:
                        raise ValueError("Transversal decomposition failed")
                return res

            v_h_ok = True
            n_order = N.order()
            for h in H.elements:
                expected = h ** n_order
                if transfer(h) != expected:
                    v_h_ok = False
                    break

            n_ker_ok = True
            id_H = Permutation()
            for n in N.elements:
                if transfer(n) != id_H:
                    n_ker_ok = False
                    break

            conclusion_holds = v_h_ok and n_ker_ok
            neg_q = not conclusion_holds

    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: G = N ⋊ H is an internal semidirect product of finite groups",
    "H_2: V: G -> H is the transfer homomorphism from G to H",
    "¬Q: The restriction of V to H is not V(h) = h^{|N|} or N is not in ker(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2
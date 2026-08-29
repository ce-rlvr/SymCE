import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
        
        G = witness.get('G')
        H = witness.get('H')
        N = witness.get('N')
        phi = witness.get('phi')
        
        # H1: G and H are groups, phi maps G to H
        try:
            h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
            if h1:
                G_elements = list(G.generate())
                H_elements = list(H.generate())
                
                if callable(phi):
                    phi_func = phi
                elif isinstance(phi, dict):
                    phi_func = lambda x: phi.get(x)
                else:
                    h1 = False
                    phi_func = None

                if h1:
                    for g in G_elements:
                        val = phi_func(g)
                        if val not in H_elements:
                            h1 = False
                            break
        except Exception:
            h1 = False

        # H2: N is a normal subgroup of G such that N \subseteq \ker(\phi)
        try:
            if h1 and isinstance(N, PermutationGroup):
                h2 = N.is_subgroup(G) and N.is_normal(G)
                if h2:
                    e_H = H.identity
                    for n in list(N.generate()):
                        if phi_func(n) != e_H:
                            h2 = False
                            break
            else:
                h2 = False
        except Exception:
            h2 = False

        # neg_Q: Conclusion fails
        # The conclusion states there exists a unique group homomorphism bar_phi: G/N -> H
        # such that phi(g) = bar_phi(gN). This holds if and only if phi itself is a homomorphism.
        # Therefore, the conclusion fails (neg_Q is True) iff phi is NOT a homomorphism.
        try:
            if h1:
                is_hom = True
                for g1 in G_elements:
                    for g2 in G_elements:
                        if phi_func(g1 * g2) != phi_func(g1) * phi_func(g2):
                            is_hom = False
                            break
                    if not is_hom:
                        break
                neg_q = not is_hom
            else:
                neg_q = False
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: N is a normal subgroup of G such that N is a subset of ker(phi)",
    "¬Q: There does not exist a unique group homomorphism bar_phi: G/N -> H such that phi(g) = bar_phi(gN)"
]

N_HYP = 2
NEG_Q_INDEX = 2
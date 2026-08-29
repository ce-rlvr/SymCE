import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup([
    Permutation([[0, 1], [2, 3]]), 
    Permutation([[0, 2], [1, 3]])
])
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = PermutationGroup([Permutation(0)])

CONDITION_LABELS = [
    "H_1: E is an intermediate field between F and K",
    "H_2: H is the subgroup Gal(K/E) of the Galois group G = Gal(K/F)",
    "¬Q: The normal closure of E over F inside K does NOT correspond to the core of H in G"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    """
    Check the counterexample for the false Galois correspondence conjecture.
    
    The witness should be a tuple (G_L, U, V) of SymPy PermutationGroup objects, where:
      - G_L represents the Galois group of the Galois closure L over F.
      - U represents the intermediate field K (i.e., K = Fix(U)).
      - V represents the intermediate field E (i.e., E = Fix(V)).
      
    The hypotheses are:
      - E is an intermediate field between F and K (so U <= V <= G_L).
      - H is the subgroup Gal(K/E) of the Galois group G = Gal(K/F).
        (In our group-theoretic model, G = N_{G_L}(U)/U and H = N_V(U)/U).
    """
    try:
        if not isinstance(witness, tuple) or len(witness) != 3:
            return [False, False, False]
        G_L, U, V = witness
        
        # H_2: Valid permutation groups (structurally guarantees H <= G in our model)
        try:
            h2 = isinstance(G_L, PermutationGroup) and isinstance(U, PermutationGroup) and isinstance(V, PermutationGroup)
        except Exception:
            h2 = False
            
        # H_1: U <= V <= G_L (E is an intermediate field between F and K)
        try:
            if h2:
                GL_elems = set(G_L.elements)
                V_elems = set(V.elements)
                U_elems = set(U.elements)
                h1 = all(u in V_elems for u in U.generators) and all(v in GL_elems for v in V.generators)
            else:
                h1 = False
        except Exception:
            h1 = False
            
        # ¬Q: The normal closure of E over F inside K does NOT correspond to the core of H in G
        try:
            if not h2:
                neg_q = False
            else:
                # W represents the normal closure of E over F inside K.
                # It corresponds to the intersection of g V g^-1 for g in G_L such that U <= g V g^-1.
                W_elements = None
                for g in GL_elems:
                    g_inv = ~g
                    gVg = set(g * v * g_inv for v in V_elems)
                    # Check if U <= g V g^-1 (i.e., the conjugate field is inside K)
                    if U_elems.issubset(gVg):
                        if W_elements is None:
                            W_elements = gVg
                        else:
                            W_elements = W_elements.intersection(gVg)
                if W_elements is None:
                    W_elements = set(GL_elems)
                    
                # C represents the core of H in G, lifted to N_{G_L}(U).
                # N_{G_L}(U) corresponds to G = Gal(K/F)
                N_GL_U = set(g for g in GL_elems if all((g * u * ~g) in U_elems for u in U.generators))
                # N_V(U) corresponds to H = Gal(K/E)
                N_V_U = set(v for v in V_elems if all((v * u * ~v) in U_elems for u in U.generators))
                
                C_elements = None
                for x in N_GL_U:
                    x_inv = ~x
                    xHx = set(x * h * x_inv for h in N_V_U)
                    if C_elements is None:
                        C_elements = xHx
                    else:
                        C_elements = C_elements.intersection(xHx)
                if C_elements is None:
                    C_elements = N_GL_U
                    
                # The conclusion holds iff the two fields are the same, which means their corresponding subgroups are equal.
                # The negation of the conclusion is that they are NOT equal.
                neg_q = (W_elements != C_elements)
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]
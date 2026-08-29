import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from itertools import permutations

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

def is_k_transitive(G, k, domain):
    if k < 0:
        return False
    if k == 0:
        return True
    if k > len(domain):
        return False
    k_tuples = list(permutations(domain, k))
    if not k_tuples:
        return True
    orbit = set()
    queue = [k_tuples[0]]
    orbit.add(k_tuples[0])
    gens = G.generators
    if not gens:
        return len(orbit) == len(k_tuples)
    while queue:
        curr = queue.pop(0)
        for g in gens:
            nxt = tuple(g(x) if isinstance(x, int) and x < g.size else x for x in curr)
            if nxt not in orbit:
                orbit.add(nxt)
                queue.append(nxt)
    return len(orbit) == len(k_tuples)

def get_stabilizer(G, alpha):
    if isinstance(alpha, int) and alpha < G.degree:
        return G.stabilizer(alpha)
    return G

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                G, k = witness
                domain = list(range(G.degree))
            elif len(witness) == 3:
                G, k, domain = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        # H_1: G is a permutation group acting on a set \Omega
        try:
            h1 = isinstance(G, PermutationGroup) and isinstance(domain, (list, set, tuple))
        except Exception:
            h1 = False
            
        # H_2: The cardinality of \Omega is at least k
        try:
            h2 = len(domain) >= k
        except Exception:
            h2 = False
            
        # ¬Q: G is k-transitive on \Omega iff G is transitive on \Omega and for any \alpha \in \Omega, G_\alpha acts (k-1)-transitively on \Omega \setminus \{\alpha\}
        try:
            domain_list = list(domain)
            lhs = is_k_transitive(G, k, domain_list)
            
            rhs_part1 = is_k_transitive(G, 1, domain_list)
            rhs_part2 = True
            for alpha in domain_list:
                G_alpha = get_stabilizer(G, alpha)
                domain_minus_alpha = [x for x in domain_list if x != alpha]
                if not is_k_transitive(G_alpha, k - 1, domain_minus_alpha):
                    rhs_part2 = False
                    break
            rhs = rhs_part1 and rhs_part2
            
            neg_q = (lhs != rhs)
        except Exception:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: G is a permutation group acting on a set \\Omega",
    "H_2: The cardinality of \\Omega is at least k",
    "¬Q: The recursive characterization of k-transitivity fails at the witness"
]

N_HYP = 2
NEG_Q_INDEX = 2
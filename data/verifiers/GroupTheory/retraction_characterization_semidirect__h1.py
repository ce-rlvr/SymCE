import itertools

# Top-level setup for standard named objects
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

def conditions(witness) -> list[bool]:
    """
    Given a witness (G, N), checks if it is a counterexample to the false conjecture.
    Returns [H1_ok, neg_Q_ok].
    """
    try:
        G, N = witness
        G_elements = list(G.elements)
        N_elements = list(N.elements)
        id_elem = G.identity
    except Exception:
        return [False, False]

    # H1: N is a normal subgroup of G
    try:
        h1 = True
        # Check if N is a subgroup
        for a in N_elements:
            for b in N_elements:
                if a * b not in N_elements:
                    h1 = False
                    break
            if not h1:
                break
        if h1 and id_elem not in N_elements:
            h1 = False
        if h1:
            for a in N_elements:
                has_inv = False
                for b in N_elements:
                    if a * b == id_elem and b * a == id_elem:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
        # Check normality: gN == Ng for all g in G
        if h1:
            for g in G_elements:
                gN = set([g * n for n in N_elements])
                Ng = set([n * g for n in N_elements])
                if gN != Ng:
                    h1 = False
                    break
    except Exception:
        h1 = False

    # Conclusion Q: G is an internal semidirect product of N and some subgroup H
    # iff there exists an endomorphism pi: G -> G such that pi(pi(g)) = pi(g) and ker(pi) = N
    try:
        n_G = len(G_elements)
        n_N = len(N_elements)
        
        # Find all subgroups of G
        cyclic_subgroups = set()
        for g in G_elements:
            H = set([id_elem])
            curr = g
            while curr not in H:
                H.add(curr)
                curr = curr * g
            cyclic_subgroups.add(frozenset(H))
                
        all_subgroups = set(cyclic_subgroups)
        added = True
        while added:
            added = False
            new_subgroups = set()
            for H1 in all_subgroups:
                for H2 in cyclic_subgroups:
                    new_H = set(H1)
                    new_H.update(H2)
                    while True:
                        size_before = len(new_H)
                        new_H.update([a * b for a in new_H for b in new_H])
                        if len(new_H) == size_before:
                            break
                    new_H_frozen = frozenset(new_H)
                    if new_H_frozen not in all_subgroups and new_H_frozen not in new_subgroups:
                        new_subgroups.add(new_H_frozen)
                        added = True
            all_subgroups.update(new_subgroups)

        # Check P: G is an internal semidirect product of N and some subgroup H
        p_holds = False
        if n_G % n_N == 0:
            target_H_size = n_G // n_N
            for H in all_subgroups:
                if len(H) == target_H_size:
                    if len(H.intersection(N_elements)) == 1:
                        NH = set()
                        for n in N_elements:
                            for h in H:
                                NH.add(n * h)
                        if len(NH) == n_G:
                            p_holds = True
                            break

        # Check Q: there exists an endomorphism pi: G -> G such that pi(pi(g)) = pi(g) and ker(pi) = N
        q_holds = False
        if n_G % n_N == 0:
            target_H_size = n_G // n_N
            for H in all_subgroups:
                if len(H) == target_H_size:
                    if len(H.intersection(N_elements)) == 1:
                        NH = set()
                        for n in N_elements:
                            for h in H:
                                NH.add(n * h)
                        if len(NH) != n_G:
                            continue
                            
                        pi_map = {}
                        for n in N_elements:
                            for h in H:
                                pi_map[n * h] = h
                                
                        is_homo = True
                        for x in G_elements:
                            for y in G_elements:
                                if pi_map[x * y] != pi_map[x] * pi_map[y]:
                                    is_homo = False
                                    break
                            if not is_homo:
                                break
                        if is_homo:
                            q_holds = True
                            break

        # The conclusion is P <-> Q
        conclusion_holds = (p_holds == q_holds)
        neg_q = not conclusion_holds

    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "¬Q: G is an internal semidirect product of N and some subgroup H iff there exists an endomorphism pi: G -> G such that pi(pi(g)) = pi(g) and ker(pi) = N is FALSE"
]

N_HYP = 1
NEG_Q_INDEX = 1
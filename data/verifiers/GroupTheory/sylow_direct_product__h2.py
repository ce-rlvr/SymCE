import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime number",
    "¬Q: A subgroup of G x H is a Sylow p-subgroup iff it is P x Q for Sylow p-subgroups P of G and Q of H"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        G, H, p = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a finite group
    try:
        h1_ok = hasattr(G, 'is_group') and G.is_group and getattr(G, 'is_finite', True)
    except Exception:
        h1_ok = False
        
    # H_2: p is a prime number
    try:
        from sympy import isprime
        h2_ok = isprime(p)
    except Exception:
        h2_ok = False
        
    # neg_Q: The conclusion fails
    try:
        # If H is not a finite group, the conclusion fails or is inapplicable
        if not (hasattr(H, 'is_group') and H.is_group and getattr(H, 'is_finite', True)):
            neg_q_ok = True
        else:
            degG = G.degree if G.degree > 0 else 1
            degH = H.degree if H.degree > 0 else 1
            
            def get_all_sylow(grp, p_val):
                P = grp.sylow_subgroup(p_val)
                P_elems = frozenset(P.elements)
                syls = set([P_elems])
                queue = [P_elems]
                while queue:
                    curr = queue.pop(0)
                    for g in grp.generators:
                        conj = frozenset([g * x * (~g) for x in curr])
                        if conj not in syls:
                            syls.add(conj)
                            queue.append(conj)
                return list(syls)
                
            syls_G = get_all_sylow(G, p)
            syls_H = get_all_sylow(H, p)
            
            gens = []
            for g in G.generators:
                a = list(g.array_form)
                if len(a) < degG: 
                    a += list(range(len(a), degG))
                a += list(range(degG, degG + degH))
                gens.append(Permutation(a))
                
            for h in H.generators:
                a = list(range(degG))
                b = list(h.array_form)
                if len(b) < degH: 
                    b += list(range(len(b), degH))
                a += [x + degG for x in b]
                gens.append(Permutation(a))
                
            if not gens:
                GxH = PermutationGroup([Permutation(degG + degH - 1)])
            else:
                GxH = PermutationGroup(gens)
                
            syls_GxH = get_all_sylow(GxH, p)
            
            def combine(g, h, dG, dH):
                a = list(g.array_form)
                if len(a) < dG: 
                    a += list(range(len(a), dG))
                b = list(h.array_form)
                if len(b) < dH: 
                    b += list(range(len(b), dH))
                return Permutation(a + [x + dG for x in b])
                
            PxQ_syls = []
            for P_sub in syls_G:
                for Q_sub in syls_H:
                    PxQ = frozenset([combine(g, h, degG, degH) for g in P_sub for h in Q_sub])
                    PxQ_syls.append(PxQ)
                    
            all_PxQ_are_syl = all(PxQ in syls_GxH for PxQ in PxQ_syls)
            all_syl_are_PxQ = all(syl in PxQ_syls for syl in syls_GxH)
            
            q_ok = all_PxQ_are_syl and all_syl_are_PxQ
            neg_q_ok = not q_ok
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]
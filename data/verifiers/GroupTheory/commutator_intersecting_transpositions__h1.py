import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness):
    h1 = False
    h2 = False
    h3 = False
    neg_q = False
    
    try:
        tau1, tau2 = None, None
        if isinstance(witness, dict):
            tau1 = witness.get('tau1')
            tau2 = witness.get('tau2')
            if tau1 is None or tau2 is None:
                perms = [v for k, v in witness.items() if isinstance(v, Permutation)]
                if len(perms) >= 2:
                    tau1, tau2 = perms[0], perms[1]
        elif isinstance(witness, (list, tuple)):
            perms = [x for x in witness if isinstance(x, Permutation)]
            if len(perms) >= 2:
                tau1 = perms[0]
                tau2 = perms[1]
                
        if not (isinstance(tau1, Permutation) and isinstance(tau2, Permutation)):
            return [False, False, False, False]
            
        h1 = True
        
        moved1 = set(i for i in range(tau1.size) if tau1(i) != i)
        moved2 = set(i for i in range(tau2.size) if tau2(i) != i)
        
        is_t1 = (len(moved1) == 2 and tau1.order() == 2)
        is_t2 = (len(moved2) == 2 and tau2.order() == 2)
        
        if is_t1 and is_t2:
            intersect = moved1.intersection(moved2)
            union = moved1.union(moved2)
            if len(intersect) == 1 and len(union) == 3:
                h2 = True
                h3 = True
            else:
                h2 = False
                h3 = False
        else:
            h2 = False
            h3 = False
            
        comm = tau1 * tau2 * (tau1**-1) * (tau2**-1)
        cycles = comm.cyclic_form
        
        is_3_cycle = (len(cycles) == 1 and len(cycles[0]) == 3)
        
        neg_q = not is_3_cycle
        
    except Exception:
        pass
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: tau1 and tau2 are permutations in S_n",
    "H_2: a, b, c are three distinct elements",
    "H_3: tau1 and tau2 are transpositions intersecting at one element",
    "not Q: The commutator of tau1 and tau2 is not a 3-cycle"
]

N_HYP = 3
NEG_Q_INDEX = 3
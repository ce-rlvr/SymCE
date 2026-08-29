import sympy
from sympy import Dummy, groebner, reduced, simplify
from sympy.abc import x, y, z, t, u, v, w
from sympy.ntheory import factorint
import math

class PolynomialRingIdealWitness:
    def __init__(self, variables, K_gens, I_gens, P_gens, Q_gens):
        """
        Represents a witness in the quotient ring R = Q[variables] / <K_gens>.
        I_gens, P_gens, Q_gens are lists of polynomials generating the ideals I, P, Q in R.
        """
        self.vars = variables
        self.K = K_gens
        self.I = I_gens
        self.P = P_gens
        self.Q = Q_gens

class ZIdealWitness:
    def __init__(self, I_gen, P_gen, Q_gen):
        """
        Represents a witness in the ring of integers Z.
        I_gen, P_gen, Q_gen are integers (or lists of integers) generating the ideals I, P, Q.
        """
        self.I = I_gen
        self.P = P_gen
        self.Q = Q_gen

def conditions(witness) -> list[bool]:
    h1 = True
    h2 = True
    h3 = False
    neg_q = False
    
    try:
        is_poly = False
        if isinstance(witness, PolynomialRingIdealWitness):
            vars_list = witness.vars
            K = witness.K
            I = witness.I
            P = witness.P
            Q = witness.Q
            is_poly = True
        elif isinstance(witness, dict) and 'vars' in witness:
            vars_list = witness['vars']
            K = witness.get('K', [])
            I = witness['I']
            P = witness['P']
            Q = witness['Q']
            is_poly = True
        elif isinstance(witness, ZIdealWitness):
            I = witness.I
            P = witness.P
            Q = witness.Q
            is_poly = False
        elif isinstance(witness, dict) and 'vars' not in witness:
            I = witness['I']
            P = witness['P']
            Q = witness['Q']
            is_poly = False
        else:
            return [False, False, False, False]
            
        if is_poly:
            I = I if isinstance(I, (list, tuple)) else [I]
            P = P if isinstance(P, (list, tuple)) else [P]
            Q = Q if isinstance(Q, (list, tuple)) else [Q]
            K = K if isinstance(K, (list, tuple)) else [K]
            
            def clean_gens(gens):
                res = []
                for g in gens:
                    sg = simplify(g)
                    if sg != 0:
                        res.append(sg)
                return res
                
            I = clean_gens(I)
            P = clean_gens(P)
            Q = clean_gens(Q)
            K = clean_gens(K)
            
            vars_for_gb = list(vars_list)
            if not vars_for_gb:
                vars_for_gb = [Dummy('dummy')]
                
            # H3: I \subseteq P
            if not P + K:
                h3 = (len(I) == 0)
            else:
                G_P = groebner(P + K, *vars_for_gb)
                G_P_list = list(G_P)
                h3 = True
                for a in I:
                    if reduced(a, G_P_list, *vars_for_gb)[1] != 0:
                        h3 = False
                        break
                        
            # neg_Q: I \not\subseteq \sqrt{Q}
            # By Rabinowitsch trick, a \in \sqrt{Q} iff 1 \in <Q, 1 - t*a>
            t_dummy = Dummy('t')
            new_vars = list(vars_list) + [t_dummy]
            
            neg_q = False
            for a in I:
                new_gens = list(Q) + list(K) + [1 - t_dummy * a]
                G_Q = groebner(new_gens, *new_vars)
                G_Q_list = list(G_Q)
                if reduced(1, G_Q_list, *new_vars)[1] != 0:
                    neg_q = True
                    break
                    
        else:
            # ZIdealWitness
            def get_int_gen(val):
                if isinstance(val, (list, tuple)):
                    g = 0
                    for v in val:
                        g = math.gcd(g, int(v))
                    return g
                return int(val)
                
            I = get_int_gen(I)
            P = get_int_gen(P)
            Q = get_int_gen(Q)
            
            # H3: I \subseteq P <=> P divides I
            if P == 0:
                h3 = (I == 0)
            else:
                h3 = (I % P == 0)
                
            # neg_Q: I \not\subseteq \sqrt{Q}
            if Q == 0:
                neg_q = (I != 0)
            else:
                factors = factorint(abs(Q))
                radical = 1
                for p in factors:
                    radical *= p
                neg_q = (I % radical != 0)
                
    except Exception:
        return [False, False, False, False]
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I is a finitely generated ideal of R",
    "H_3: I is a subset of P",
    "¬Q: For all positive integers n, I^n is not a subset of Q"
]

N_HYP = 3
NEG_Q_INDEX = 3
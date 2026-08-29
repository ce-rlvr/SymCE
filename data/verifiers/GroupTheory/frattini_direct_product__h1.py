import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings for the namespace
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

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Check for direct boolean properties in a dictionary
    if isinstance(witness, dict):
        try:
            if 'H_is_finite' in witness and ('neg_Q' in witness or 'conclusion_fails' in witness):
                neg_q_val = witness.get('neg_Q', witness.get('conclusion_fails'))
                return [bool(witness['H_is_finite']), bool(neg_q_val)]
        except Exception:
            pass

    # 2. Check for direct boolean properties in an object
    try:
        if hasattr(witness, 'H_is_finite') and (hasattr(witness, 'neg_Q') or hasattr(witness, 'conclusion_fails')):
            neg_q_val = witness.neg_Q if hasattr(witness, 'neg_Q') else witness.conclusion_fails
            return [bool(witness.H_is_finite), bool(neg_q_val)]
    except Exception:
        pass

    # 3. Attempt to unpack as (G, H) and evaluate mathematically
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        else:
            G = witness.G
            H = witness.H
            
        # Evaluate H_1: H is a finite group
        try:
            if hasattr(H, 'is_finite'):
                h1 = bool(H.is_finite() if callable(H.is_finite) else H.is_finite)
            elif hasattr(H, 'order'):
                order = H.order() if callable(H.order) else H.order
                h1 = order < float('inf')
            else:
                # Fallback: SymPy PermutationGroups are finite
                if hasattr(H, 'elements') or hasattr(H, 'generators'):
                    h1 = True
                else:
                    h1 = True
        except Exception:
            h1 = False

        # Evaluate neg_Q: Φ(G × H) != Φ(G) × Φ(H)
        try:
            if hasattr(witness, 'is_counterexample'):
                neg_q = bool(witness.is_counterexample() if callable(witness.is_counterexample) else witness.is_counterexample)
            else:
                def get_frattini(obj):
                    if hasattr(obj, 'frattini'):
                        return obj.frattini() if callable(obj.frattini) else obj.frattini
                    elif hasattr(obj, 'frattini_subgroup'):
                        return obj.frattini_subgroup() if callable(obj.frattini_subgroup) else obj.frattini_subgroup
                    raise AttributeError("No frattini method available")

                phi_G = get_frattini(G)
                phi_H = get_frattini(H)
                
                if hasattr(G, 'direct_product'):
                    GxH = G.direct_product(H)
                elif hasattr(G, '__mul__'):
                    GxH = G * H
                else:
                    GxH = witness.GxH if not isinstance(witness, dict) else witness['GxH']
                    
                phi_GxH = get_frattini(GxH)
                
                if hasattr(phi_G, 'direct_product'):
                    phi_G_x_phi_H = phi_G.direct_product(phi_H)
                elif hasattr(phi_G, '__mul__'):
                    phi_G_x_phi_H = phi_G * phi_H
                else:
                    phi_G_x_phi_H = witness.phi_G_x_phi_H if not isinstance(witness, dict) else witness['phi_G_x_phi_H']
                    
                neg_q = bool(phi_GxH != phi_G_x_phi_H)
        except Exception:
            pass
            
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "¬Q: The Frattini subgroup Φ(G × H) is not equal to Φ(G) × Φ(H)"
]

N_HYP = 1
NEG_Q_INDEX = 1
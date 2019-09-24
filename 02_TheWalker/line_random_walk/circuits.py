import numpy as np
from qiskit import QuantumRegister, QuantumCircuit

def hop_unitary(excitations_qr, phi, k, l):
    qc = QuantumCircuit(excitations_qr)
    
    qc.x(excitations_qr[k])
    qc.cx(excitations_qr[k], excitations_qr[l])
    qc.x(excitations_qr[k])
    
    qc.rz(phi, excitations_qr[k])
    qc.x(excitations_qr[l])
    qc.rx(np.pi / 4, excitations_qr[k])
    qc.cz(excitations_qr[l], excitations_qr[k])
    qc.rx(-np.pi / 4, excitations_qr[k])
    qc.cz(excitations_qr[l], excitations_qr[k])
    qc.x(excitations_qr[l])
    qc.rz(-phi, excitations_qr[k])
    
    qc.x(excitations_qr[k])
    qc.cx(excitations_qr[k], excitations_qr[k + 1])
    qc.x(excitations_qr[k])
    
    return qc

def walk_step(excitations_qr, phi, initial_position, n_swipes):
    qc = QuantumCircuit(excitations_qr)
    
    for swipe in range(n_swipes):
        left_indices = list(range(max(0, initial_position - swipe - 1), initial_position))
        right_indices = list(range(initial_position, min(initial_position + swipe + 1, len(excitations_qr) - 1)))
        #print ("swipe: {} | left indices: {} | right indices: {}".format(swipe, left_indices, right_indices))
        #for k in left_indices + right_indices:
        for k in right_indices + left_indices:
            qc += hop_unitary(excitations_qr, phi, k, k + 1)
            
    return qc

def potential_step(excitations_qr, values, t):
    qc = QuantumCircuit(excitations_qr)
    
    for k, h in enumerate(values):
        qc.rz(t * h, excitations_qr[k])
    
    return qc
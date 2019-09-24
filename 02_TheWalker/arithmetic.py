from qiskit import QuantumCircuit, QuantumRegister

def extract_quantum_registers(*regs):
    return list(set([ reg if type(reg) == QuantumRegister else reg[0] for reg in regs ]))

def nested_ccx(qc, target_qr, control_qr, ancilla_qr):
    if len(control_qr) == 1:
        qc.cx(control_qr[0], target_qr)
    elif len(control_qr) == 2:
        qc.ccx(control_qr[0], control_qr[1], target_qr)
    else:
        qc.ccx(control_qr[-1], ancilla_qr[-1], target_qr)
        inner_qc = nested_ccx(qc, ancilla_qr[-1], control_qr[:-1], ancilla_qr[:-1])
        qc.ccx(control_qr[-1], ancilla_qr[-1], target_qr)

# See 0408173v2, page 5
def mcx(qc, target_qr, control_data, ancilla_qr):
    control_qr = [ q for q, flip_value in control_data ]
    for q, flip_value in control_data:
        if not flip_value:
            qc.x(q)
    nested_ccx(qc, target_qr, control_qr, ancilla_qr)
    if len(control_qr) > 2:
        nested_ccx(qc, ancilla_qr[-1], control_qr[:-1], ancilla_qr[:-1])
    for q, flip_value in control_data:
        if not flip_value:
            qc.x(q)

def mc_add_classical_bit(qc, control_bits, cbit, result_qr, carry_qr, cond_qr, ancilla_qr=None):
    if not cbit:
        return qc
    
    control_list = [ (q, 1) for q in control_bits ]
    
    for i in range(len(result_qr)):
        # Propagate the carry depending on the value of the i-th bit of the current result
        
        if i == 0:
            mcx(qc, carry_qr[i], control_list + [ (result_qr[i], 1) ], ancilla_qr)
        elif i < len(result_qr) - 1:
            mcx(qc, cond_qr, control_list + [ (result_qr[i], 1) ], ancilla_qr)
            mcx(qc, carry_qr[i], control_list + [ (cond_qr, 1), (carry_qr[i - 1], 1) ], ancilla_qr)
            mcx(qc, cond_qr, control_list + [ (result_qr[i], 1) ], ancilla_qr)
            
        # XOR the current result bit with the bit to add
        
        if i == 0:
            mcx(qc, result_qr[i], control_list, ancilla_qr)
        else:
            mcx(qc, result_qr[i], control_list + [ (carry_qr[i - 1], 1) ], ancilla_qr)
    
    # Uncompute carries
    
    for i in range(len(result_qr) - 2, -1, -1):
        if i == 0:
            mcx(qc, carry_qr[i], control_list + [ (result_qr[i], 0) ], ancilla_qr)
        else:
            mcx(qc, cond_qr, control_list + [ (result_qr[i], 0) ], ancilla_qr)
            mcx(qc, carry_qr[i], control_list + [ (cond_qr, 1), (carry_qr[i - 1], 1) ], ancilla_qr)
            mcx(qc, cond_qr, control_list + [ (result_qr[i], 0) ], ancilla_qr)
        
    return qc

def mc_add_classical(qc, control_bits, summand, result_qr, carry_qr, cond_qr, ancilla_qr=None):
    for i in range(max(len(result_qr), len(carry_qr))):
        mc_add_classical_bit(qc, control_bits, (summand & 1), result_qr[i:], carry_qr, cond_qr, ancilla_qr)
        summand = summand >> 1

def mc_subtract_classical(qc, control_bits, summand, result_qr, carry_qr, cond_qr, ancilla_qr=[]):
    # TODO: remove call to extract_quantum_registers if QuantumCircuit() is updated to handle register specifications of type (QuantumRegister, 0) instead of only QuantumRegister
    regs = [ result_qr, carry_qr, cond_qr, *ancilla_qr ]
    if len(control_bits) > 0:
        regs += [ *control_bits ]
    new_qc = QuantumCircuit(*extract_quantum_registers(*regs))
    mc_add_classical(new_qc, control_bits, summand, result_qr, carry_qr, cond_qr, ancilla_qr)
    qc += new_qc.inverse()
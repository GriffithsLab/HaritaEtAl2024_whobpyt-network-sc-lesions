"""
Authors: Zheng Wang, John Griffiths, Andrew Clappison, Hussain Ather
Neural Mass Model fitting
module for model parameters inital values
"""


class ParamsModel:

    def __init__(self, model_name, **kwargs):
        param = {'g': [100, 0]}

        if model_name == 'RWW':
            param = {

                "std_in": [0.02, 0],  # standard deviation of the Gaussian noise
                "std_out": [0.02, 0],  # standard deviation of the Gaussian noise
                # Parameters for the ODEs
                # Excitatory population
                "W_E": [1., 0],  # scale of the external input
                "tau_E": [100., 0],  # decay time
                "gamma_E": [0.641 / 1000., 0],  # other dynamic parameter (?)

                # Inhibitory population
                "W_I": [0.7, 0],  # scale of the external input
                "tau_I": [10., 0],  # decay time
                "gamma_I": [1. / 1000., 0],  # other dynamic parameter (?)

                # External input
                "I_0": [0.32, 0],  # external input
                "I_external": [0., 0],  # external stimulation

                # Coupling parameters
                "g": [20., 0],  # global coupling (from all nodes E_j to single node E_i)
                "g_EE": [.1, 0],  # local self excitatory feedback (from E_i to E_i)
                "g_IE": [.1, 0],  # local inhibitory coupling (from I_i to E_i)
                "g_EI": [0.1, 0],  # local excitatory coupling (from E_i to I_i)

                "aE": [310, 0],
                "bE": [125, 0],
                "dE": [0.16, 0],
                "aI": [615, 0],
                "bI": [177, 0],
                "dI": [0.087, 0],

                # Output (BOLD signal) # check friston et al., (2000) and the DCM paper, friston et al., (2003) for variable names/values. See  Mechelli et al., (2000) for value ranges. 

                "alpha": [0.32, 0], # parameter = 'stiffness'
                "rho": [0.34, 0], # rho and E0 are the same. Some publications switch the variables but they mean the same thing. 
                "k1": [2.38, 0], # k1, k2, k3 are in the equations.
                "k2": [2.0, 0], # they can be calculated based on the E0 value. 
                "k3": [0.48, 0],  
                "V": [.02, 0], # V0 --> parameter = resting blood volume fraction
                "E0": [0.34, 0], # parameter = oxygen extraction
                "tau_s": [1 / 0.65, 0], # 1.54 --> parameter = signal decay
                "tau_f": [1 / 0.41, 0], # 2.44 --> parameter = autoregulation
                "tau_0": [0.98, 0], # parameter = transit time
                "mu": [0.5, 0] # I am assuming this is neuronal efficacy denoted by '∊'

            }
        elif model_name == "JR":
            param = {
                "A ": [3.25, 0], "a": [100, 0.], "B": [22, 0], "b": [50, 0], "g": [1000, 0],
                "c1": [135, 0.], "c2": [135 * 0.8, 0.], "c3 ": [135 * 0.25, 0.], "c4": [135 * 0.25, 0.],
                "std_in": [100, 0], "vmax": [5, 0], "v0": [6, 0], "r": [0.56, 0], "y0": [2, 0],
                "mu": [.5, 0], "k": [5, 0], "cy0": [5, 0], "ki": [1, 0]
            }
        for var in param:
            setattr(self, var, param[var])

        for var in kwargs:
            setattr(self, var, kwargs[var])

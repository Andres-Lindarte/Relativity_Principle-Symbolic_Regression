import numpy as np
import pandas as pd
import random

C_VEL = 3e8 #m/s

class data_generator:
    def __init__(self, VEL_RANGE:tuple, SEED:float = 42, N_SAMPLES:int = 1000, COORD_RANGE:tuple = (0.0, 100.0)):
        self.vel_range = VEL_RANGE
        self.seed = SEED
        self.n_samples = N_SAMPLES
        self.coord_range = COORD_RANGE

    def rel_velocity(self):
        min_range = self.vel_range[0]
        max_range = self.vel_range[1]
        random.seed(self.seed)
        proportion = random.uniform(min_range, max_range)
        return C_VEL*proportion

    def sigma_coordenates(self):
        min_range = self.coord_range[0]
        max_range = self.coord_range[1]
        x0 = random.uniform(min_range, max_range)
        x1 = random.uniform(min_range, max_range)
        return x0, x1

    def calculate_sigma_prime(self, rel_vel, x0, x1):
        beta = (rel_vel)/(C_VEL)
        gamma = 1/(np.sqrt(1.0 - (beta**2)))

        # Generate the coordenates for sigma prime
        x0p = gamma*(x0 - beta*x1)
        x1p = gamma*(x1 - beta*x0)

        # Add noise to the data
        random.seed(self.seed)
        noise_x0p = random.normal(x0p, 0.01)
        noise_x1p = random.normal(x1p, 0.01)

        x0p_with_noise = x0p + noise_x0p
        x1p_with_noise = x1p + noise_x1p

        return x0p_with_noise, x1p_with_noise


    def generate_data(self):
        rows = []
        while len(rows) < self.n_samples:
            rel_v = self.rel_velocity()
            x0, x1 = self.sigma_coordenates()
            x0p_n, x1p_n = self.calculate_sigma_prime(rel_v, x0, x1)

            rows.append({
                'rel_vel': rel_v ,
                'x0': x0 , 
                'x1': x1 ,
                # Target
                'x0p_noise': x0p_n , 
                'x1p_noise': x1p_n , 
            })
        return pd.DataFrame(rows)

    def print_data_txt(self, data):
        fout = open(f"data/data_({self.vel_range[0]}, {self.vel_range[1]})_{self.seed}.txt", "w") # Open a file to write the results
        fout 
            
"""
Needs: 
    range:float, 
    seed:float, 
    N_samples:int
What does it do?: 
    - Generates relative velocity (v)
    - Generates (x^0, x^1) SIGMA
    - Calculate (x'^0, x'^1) SIGAM' with (v) 
    - Generate DataFrame
    - Print to text file
"""
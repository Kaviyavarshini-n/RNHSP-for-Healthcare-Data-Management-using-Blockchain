import numpy as np
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import pandas as pd
def fitness_function(x):
    return np.sum(x**2)

def opposition_based_population(population, lower_bound, upper_bound):
    return lower_bound + upper_bound - population

def decrypt_data(attribute_key, ciphertext, iv):
    key = str(attribute_key).encode('utf-8')
    key = key.ljust(32, b'\0')[:32]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    try:
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    except ValueError as e:
        print(f"Decryption failed for key: {key} and IV: {iv.hex()}")
        raise e
    
    return padded_plaintext

def load_and_decrypt_data(file_path,original_health_data):
    encrypted_df = pd.read_csv(file_path)
    decrypted_data = []
    for index, row in encrypted_df.iterrows():
        original_row = original_health_data[original_health_data['Name'] == row['Name']]
        if original_row.empty:
            print(f"Age not found for {row['Name']}")
            continue
        attribute_key = original_row['Age'].values[0]
        encrypted_data = bytes.fromhex(row['Encrypted Data'])
        iv = bytes.fromhex(row['IV'])
        decrypted_value = decrypt_data(attribute_key, encrypted_data, iv)
        decrypted_data.append(decrypted_value)
    
    return decrypted_data
    
class OBL:
    def __init__(self, n_particles, dim, lower_bound, upper_bound, max_iter, decrypted_data):
        self.n_particles = n_particles
        self.dim = dim
        self.lower_bound = lower_bound
        self.upper_bound = upper_bound
        self.max_iter = max_iter
        self.inertia = 0.7
        self.c1 = 1.5
        self.c2 = 1.5
        self.population = np.random.uniform(self.lower_bound, self.upper_bound, (self.n_particles, self.dim))
        self.velocities = np.random.uniform(-1, 1, (self.n_particles, self.dim))
        self.pbest_positions = self.population.copy()
        self.pbest_fitness = np.apply_along_axis(fitness_function, 1, self.population)
        self.gbest_position = self.pbest_positions[np.argmin(self.pbest_fitness)]
        self.gbest_fitness = np.min(self.pbest_fitness)
        self.decrypted_data = decrypted_data

    def optimize(self):
        for iteration in range(self.max_iter):
            opposition_population = opposition_based_population(self.population, self.lower_bound, self.upper_bound)
            opposition_fitness = np.apply_along_axis(fitness_function, 1, opposition_population)
            combined_population = np.vstack((self.population, opposition_population))
            combined_fitness = np.hstack((np.apply_along_axis(fitness_function, 1, self.population), opposition_fitness))
            best_indices = np.argsort(combined_fitness)[:self.n_particles]
            self.population = combined_population[best_indices]
            self.pbest_positions = self.population.copy()
            self.pbest_fitness = np.apply_along_axis(fitness_function, 1, self.population)
            self.gbest_position = self.pbest_positions[np.argmin(self.pbest_fitness)]
            self.gbest_fitness = np.min(self.pbest_fitness)
            for i in range(self.n_particles):
                r1 = np.random.rand(self.dim)
                r2 = np.random.rand(self.dim)
                cognitive_velocity = self.c1 * r1 * (self.pbest_positions[i] - self.population[i])
                social_velocity = self.c2 * r2 * (self.gbest_position - self.population[i])
                self.velocities[i] = self.inertia * self.velocities[i] + cognitive_velocity + social_velocity
                self.population[i] = self.population[i] + self.velocities[i]

            self.population = np.clip(self.population, self.lower_bound, self.upper_bound)
            fitness_values = np.apply_along_axis(fitness_function, 1, self.population)
            for i in range(self.n_particles):
                if fitness_values[i] < self.pbest_fitness[i]:
                    self.pbest_fitness[i] = fitness_values[i]
                    self.pbest_positions[i] = self.population[i]
            if np.min(fitness_values) < self.gbest_fitness:
                self.gbest_fitness = np.min(fitness_values)
                self.gbest_position = self.population[np.argmin(fitness_values)]

            print(f"Iteration {iteration + 1}/{self.max_iter}, Global Best Fitness: {self.gbest_fitness}\n")

        return self.gbest_position, self.gbest_fitness

if __name__ == "__main__":
    print(f"\n=========================\n  Optimisation started:\n=========================\n")
    time.sleep(2)
    original_health_data = pd.read_csv('user_health_data.csv')
    decrypted_data = load_and_decrypt_data('encrypted_health_data.csv',original_health_data)
    n_particles = 50
    dim = 10
    lower_bound = -10
    upper_bound = 10
    max_iter = 50
    OBL = OBL(n_particles, dim, lower_bound, upper_bound, max_iter, decrypted_data)
    best_position, best_fitness = OBL.optimize()
    time.sleep(2)
    print(f"\n=====================\n  Optimal Position:\n=====================\n {best_position}")
    time.sleep(2)
    print(f"\n====================\n  Optimal Fitness:\n====================\n {best_fitness}")

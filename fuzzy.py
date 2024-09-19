import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

def create_fuzzy_variables():
    surface = ctrl.Antecedent(np.arange(0, 6, 1), 'surface')
    dirt = ctrl.Antecedent(np.arange(0, 6, 1), 'dirt')

    suction = ctrl.Consequent(np.arange(0, 11, 1), 'suction')

    surface['easy'] = fuzz.trimf(surface.universe, [0, 0, 2])
    surface['moderate'] = fuzz.trimf(surface.universe, [2, 3, 4])
    surface['difficult'] = fuzz.trimf(surface.universe, [3, 5, 5])

    dirt['light'] = fuzz.trimf(dirt.universe, [0, 0, 2])
    dirt['moderate'] = fuzz.trimf(dirt.universe, [1, 3, 5])
    dirt['heavy'] = fuzz.trimf(dirt.universe, [3, 5, 5])

    suction['low'] = fuzz.trimf(suction.universe, [0, 2, 4])
    suction['medium'] = fuzz.trimf(suction.universe, [3, 5, 7])
    suction['high'] = fuzz.trimf(suction.universe, [6, 8, 10])

    return surface, dirt, suction

def create_fuzzy_rules(surface, dirt, suction):
    rule1 = ctrl.Rule(surface['easy'] & dirt['light'], suction['low'])
    rule2 = ctrl.Rule(surface['moderate'] & dirt['light'], suction['medium'])
    rule3 = ctrl.Rule(surface['difficult'] | dirt['heavy'], suction['high'])
    rule4 = ctrl.Rule(surface['moderate'], suction['medium'])
    return [rule1, rule2, rule3, rule4]

def create_control_system(rules):
    suction_ctrl = ctrl.ControlSystem(rules)
    return ctrl.ControlSystemSimulation(suction_ctrl)

def run_fuzzy_vacuum_system(surface_value, dirt_value):
    surface, dirt, suction = create_fuzzy_variables()
    rules = create_fuzzy_rules(surface, dirt, suction)
    simulation = create_control_system(rules)
    
    simulation.input['surface'] = surface_value
    simulation.input['dirt'] = dirt_value

    simulation.compute()

    plot_fuzzy_graphs(surface, dirt, suction, simulation)

    return simulation.output['suction']

def plot_fuzzy_graphs(surface, dirt, suction, simulation):
    surface.view(sim=simulation)
    dirt.view(sim=simulation)
    suction.view(sim=simulation)

    plt.show()

if __name__ == "__main__":
    surface_value = float(input("Insira o nível de dificuldade da superfície (0-5): "))
    dirt_value = float(input("Insira o nível de sujeira (0-5): "))

    result = run_fuzzy_vacuum_system(surface_value, dirt_value)
    print(f"Nível de sucção recomendada: {result:.2f}")

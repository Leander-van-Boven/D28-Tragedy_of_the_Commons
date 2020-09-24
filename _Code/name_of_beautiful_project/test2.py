import output
import numpy as np

class TestSimulation:
    def run_test_simulation(self):
        epoch = 0
        while (epoch < 100):
            yield epoch, np.random.random(), np.random.random()
            epoch += 1

sim = TestSimulation()
printer = output.ResultsPrinter()
printer.start_printer(sim.run_test_simulation)


import os.path
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))

# from mesa.batchrunner import BatchRunnerMP
from src.mesa_addons.BatchRunnerMP_timer import BatchRunnerMP
import pandas as pd

from src.model.world import World


from src.scenario.scenario_data import power_plants
import logging
import pandas as pd

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.WARNING)

"""
File name: batch_run_timer
Date created: 25/01/2019
Feature: # Functionality to time run of model at different sized countries
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"






class DemandTimer:

    def __init__(self):
        self.power_plants = power_plants


    def run_world_with_demand_and_power_plants(self):

        number_of_steps = 40
        data_folder = "timings"

        fixed_params = {
            "initialization_year": 2018,
            "number_of_steps": number_of_steps,
            "demand_change": [1.0] * 50,
            "data_folder": data_folder
        }

        variable_params = {
            # "carbon_price_scenario": [[0]*50, [10]*50, [20]*50, [30] * 50, [40]*50, [100]*50],
            "carbon_price_scenario": [[0]*50],
            "power_plants": [
                # self.stratify_data(2772),
                # self.stratify_data(4881),
                # self.stratify_data(18940),
                # self.stratify_data(37320),
                # self.stratify_data(65450),
                # self.stratify_data(94640),
                # self.stratify_data(150300),
                # self.stratify_data(322200),
                # self.stratify_data(1074000),
                # self.stratify_data(1646000)

                # self.stratify_data(277.2),
                # self.stratify_data(488.1),
                # self.stratify_data(1894.0),
                # self.stratify_data(37320),
                # self.stratify_data(65450),
                # self.stratify_data(94640),
                # self.stratify_data(150300),
                # self.stratify_data(322200),
                self.stratify_data(1070.4000),
                self.stratify_data(1640.6000)
            ]
        }



        batch_run = BatchRunnerMP(World,
                                  fixed_parameters=fixed_params,
                                  variable_parameters=variable_params,
                                  iterations=1,
                                  max_steps=number_of_steps, nr_processes=2)

        batch_run.run_all()


    def stratify_data(self, demand):
        frac_to_scale = demand/power_plants.Capacity.sum()
        stratified_sample = self.power_plants.groupby(['Fuel']).apply(lambda x: x.sample(frac=frac_to_scale, replace=True))
        return stratified_sample

if __name__ == "__main__":
    DemandTimer().run_world_with_demand_and_power_plants()

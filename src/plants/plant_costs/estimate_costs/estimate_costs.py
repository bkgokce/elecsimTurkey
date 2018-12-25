from numpy import isnan
from numpy import ndarray
import src.scenario.scenario_data as scenario
from src.plants.plant_registry import PlantRegistry
from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.fuel_plant_calculations.fuel_plants_old_params import FuelOldPlantCosts
from src.plants.plant_costs.estimate_costs.estimate_old_plant_cost_params.non_fuel_plant_calculations.non_fuel_plants_old_params import NonFuelOldPlantCosts

"""
File name: _select_cost_estimator
Date created: 01/12/2018
Feature: # Functionality to estimate costs based on year. If year is past 2018 then use modern data from BEIS file.
         # If data is historic, then predict from historic LCOE values, maintaining same ratios from 2018.
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

EARLIEST_MODERN_PLANT_YEAR = 2018



def create_power_plant(name, start_date, simplified_type, capacity):
    estimated_cost_parameters = _select_cost_estimator(start_year=start_date,
                                                       plant_type=simplified_type,
                                                       capacity=capacity)
    power_plant_obj = PlantRegistry(simplified_type).plant_type_to_plant_object()
    power_plant = power_plant_obj(name=name, plant_type=simplified_type,
                                  capacity_mw=capacity, construction_year=start_date,
                                  **estimated_cost_parameters)
    return power_plant


def _select_cost_estimator(start_year, plant_type, capacity):
    _check_digit(capacity, "capacity")
    _check_digit(start_year, "start_year")
    _check_positive(start_year, "start_year")
    _check_positive(capacity, "start_year")

    hist_costs = scenario.power_plant_historical_costs_long
    hist_costs = hist_costs[hist_costs.Technology.map(lambda x: x in plant_type)].dropna()

    if start_year < EARLIEST_MODERN_PLANT_YEAR and not hist_costs.empty:
        require_fuel = PlantRegistry(plant_type).check_if_fuel_required()
        cost_parameters = _estimate_old_plant_cost_parameters(capacity, plant_type, require_fuel, start_year)
        _check_parameters(capacity, cost_parameters, plant_type, start_year)
        return cost_parameters
    else:
        cost_parameters = PredictModernPlantParameters(plant_type, capacity, start_year).parameter_estimation()
        _check_parameters(capacity, cost_parameters, plant_type, start_year)
        return cost_parameters


def _check_parameters(capacity, cost_parameters, plant_type, start_year):
    assert not all(value == 0 for value in
                   cost_parameters.values()), "All values are 0 for cost parameters for power plant of year {}, type {}, and capacity {}".format(
        start_year, plant_type, capacity)
    assert not any(isnan(value).any() for value in
                   cost_parameters.values()), "All values are nan for cost parameters for power plant of year {}, type {}, and capacity {}".format(
        start_year, plant_type, capacity)


def _check_digit(value, string):
    if not isinstance(value, int) and not isinstance(value, float) and not isinstance(value, ndarray):
        raise ValueError("{} must be a number".format(string))

def _check_positive(variable, string):
    if variable < 0:
        raise ValueError("{} must be greater than 0. Produced is: {}".format(string, variable))


def _estimate_old_plant_cost_parameters(capacity, plant_type, require_fuel, start_year):
    if require_fuel:
        fuel_plant_parameters = FuelOldPlantCosts(start_year, plant_type, capacity)
        return fuel_plant_parameters.estimate_cost_parameters()
    else:
        non_fuel_plant_parameters = NonFuelOldPlantCosts(start_year, plant_type, capacity)
        return non_fuel_plant_parameters.get_cost_parameters()

from src.role.plants.fuel_plant_cost_calculations import FuelPlantCostCalculations
# from pytest_mock import mocker
from src.model.world import World
from unittest.mock import Mock
import pytest

import logging
logger = logging.getLogger(__name__)

"""
File name: test_fuelPlantCostCalculations
Date created: 27/12/2018
Feature: #Enter feature description here
"""
from unittest import TestCase

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"


logging.basicConfig(level=logging.DEBUG)



class TestFuelPlantCostCalculations:

    @pytest.fixture
    def mock_model(self):
        return Mock(spec=World)

    def test_short_run_marginal_cost(self, mock_model):
        mock_model.year_number=2018
        # assert mock_model.year_number == 2018
        plant_cost_calculation = FuelPlantCostCalculations(plant_type = "CCGT", capacity_mw = 1200, construction_year = 2018, average_load_factor = 0.93, efficiency = 0.54, pre_dev_period = 3,
                 construction_period = 3, operating_period = 25, pre_dev_spend_years = [0.44, 0.44, 0.12], construction_spend_years = [0.4, 0.4, 0.2],
                 pre_dev_cost_per_mw = 10000, construction_cost_per_mw = 500000, infrastructure = 15100000, fixed_o_and_m_per_mw = 12200,
                 variable_o_and_m_per_mwh = 3, insurance_cost_per_mw = 2100, connection_cost_per_mw = 3300)
        logger.debug(plant_cost_calculation.calculate_short_run_marginal_cost(mock_model))
        short_run_marginal_cost = plant_cost_calculation.calculate_short_run_marginal_cost(mock_model)
        assert short_run_marginal_cost == pytest.approx(28.1362533)


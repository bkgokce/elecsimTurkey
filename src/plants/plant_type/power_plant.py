"""power_plant.py: Class which represents a Power Plant"""

from abc import ABC, abstractmethod

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerPlant(ABC):
    def __init__(self, name, plant_type, capacity_mw, construction_year, average_load_factor, pre_dev_period, construction_period, operating_period, pre_dev_spend_years, construction_spend_years, pre_dev_cost_per_mw, construction_cost_per_mw, infrastructure, fixed_o_and_m_per_mw, variable_o_and_m_per_mwh, insurance_cost_per_mw, connection_cost_per_mw):
        """
        PowerPlant class which are built and operated by generation companies
        :param name: Name of power plant
        :param plant_type: Type of power plant
        :param capacity_mw: Capacity of power plant (MW)
        :param construction_year: Year that the power plant was constructed
        :param average_load_factor: Average amount of time that power plant is used
        :param pre_dev_period: Amount of time construction spends in pre-development
        :param construction_period: Amount of time construction spends in construction
        :param construction_spend_years: Percentage of costs that are spread over each year of construction
        :param pre_dev_spend_years: Percentage of costs that are spread over each year of pre-development
        :param operating_period: How long the power plant remains operational
        :param pre_dev_cost_per_mw: Cost of pre-development per kW of capacity
        :param construction_cost_per_mw: Cost of construction per kW of capacity
        :param infrastructure: Infrastructure cost in GBP
        :param fixed_o_and_m_per_mw: Fixed operation and maintenance cost
        :param variable_o_and_m_per_mwh: Variable operation and maintenance cost
        :param insurance_cost_per_mw: Insurance cost
        :param connection_cost_per_mw: Connection and use of system cost
        """

        # Data from BEIS
        self.name = name

        self.plant_type = plant_type

        self.capacity_mw = capacity_mw

        self.construction_year = construction_year

        self.average_load_factor = average_load_factor

        self.pre_dev_period = pre_dev_period
        self.pre_dev_spend_years = pre_dev_spend_years

        self.construction_period = construction_period
        self.construction_spend_years = construction_spend_years

        self.pre_dev_cost_per_mw = pre_dev_cost_per_mw

        self.construction_cost_per_mw = construction_cost_per_mw

        self.operating_period = operating_period

        self.infrastructure = infrastructure

        self.fixed_o_and_m_per_mw = fixed_o_and_m_per_mw

        self.variable_o_and_m_per_mwh = variable_o_and_m_per_mwh

        self.insurance_cost_per_mw = insurance_cost_per_mw

        self.connection_cost_per_mw = connection_cost_per_mw

        self.is_operating = False

        #
        # self.min_running = min_running


        # Bids
        self.accepted_bids = []

        self.capacity_fulfilled = 0

    # @property
    # def infrastructure(self):
    #     return self._infrastructure
    #
    # @infrastructure.setter
    # def infrastructure(self, value):
    #     self._infrastructure = value * constants.KW_TO_MW

    # def __init__(self, name, constructionStartTime, min_running, lifetime, down_payment, ann_cost, depreciation, operating_cost, capacity, construction_time, carbon_emissions, efficiency):
    #     # Fixed definitions
    #
    #     #
    #     self.name = name
    #
    #     # Construction details
    #     self.constructionStartTime = constructionStartTime
    #
    #
    #     self.min_running = min_running
    #     self.lifetime = lifetime
    #     self.down_payment = down_payment
    #     self.ann_cost = ann_cost
    #     self.depreciation = depreciation
    #     self.operating_cost = operating_cost
    #     self.capacity = capacity
    #     self.construction_time = construction_time
    #     self.efficiency = efficiency
    #
    #
    #     # Variable definitions
    #     self.capacity_fulfilled = 0
    #     self.CO2_emissions = carbon_emissions
    #
    #     # Bids
    #     self.accepted_bids = []


    def reset_plant_contract(self):
        self.capacity_fulfilled = 0

    @abstractmethod
    def short_run_marginal_cost(self, model):
        pass

    def __str__(self):
        ret = "Name: {}. Type: {}. Capacity: {}.".format(self.name, self.plant_type, self.capacity_mw)
        return ret

    def __repr__(self):
        return 'PowerPlant({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {})'.format(self.name, self.plant_type, self.capacity_mw, self.construction_year, self.average_load_factor, self.pre_dev_period, self.construction_period, self.operating_period, self.pre_dev_spend_years, self.construction_spend_years, self.pre_dev_cost_per_mw, self.construction_cost_per_mw, self._infrastructure, self.fixed_o_and_m_per_mw, self.variable_o_and_m_per_mwh, self.insurance_cost_per_mw, self.connection_cost_per_mw)


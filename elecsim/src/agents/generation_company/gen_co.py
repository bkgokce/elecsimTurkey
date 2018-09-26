from random import randint

from mesa import Agent

from elecsim.src.plants.power_plant import PowerPlant
from elecsim.src.power_exchange.bid import Bid

"""gen_co.py: Agent which represents a generation company"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


def create_gencos(psd):
    print(psd)


class GenCo(Agent):

    def __init__(self, unique_id, model, name="Empty", plants=None, money=5000000, carbon_tax=0):
        """
        Agent which defines a generating company
        :param unique_id: Unique ID for the generating company
        :param model:  Model which defines the world that the agent lives in
        :param name
        :param plants: Plants which the generating company is initialised with
        :param money: Money which the agent is initialised with
        """
        super().__init__(unique_id, model)
        if plants is None: plants = []

        self.plants = plants
        self.money = money
        self.name = name
        self.carbon_tax = carbon_tax

    def step(self):
        print("Stepping generation company "+str(self.unique_id))
        self.invest()
        self.reset_contracts()
        # self.make_bid()

    def calculate_bids(self, segment_hour, segment_value):
        """
        Function to generate the bids for each of the power plants owned by the generating company.
        The bids submitted are the fixed costs divided by lifetime of plant plus yearly variable costs plus a 10% margin
        :param segment_hour: Number of hours in which the current segment is required
        :param segment_value: Electricity consumption required for the specified number of hours
        :return: Bids returned for the available plants at the specified segment hour
        """
        bid = []
        for i in range(len(self.plants)):
            plant = self.plants[i]
            if plant.min_running <= segment_hour and plant.capacity_fulfilled < plant.capacity:
                # price = ((plant.down_payment/plant.lifetime + plant.ann_cost + plant.operating_cost)/(plant.capacity*segment_hour))*1.1
                price = plant.calculate_lcoe
                bid.append(Bid(self, plant, segment_hour, plant.capacity-plant.capacity_fulfilled, price))
        return bid

    # def purchase_fuel(self):

    def invest(self):
        # plant_to_invest = PowerPlant(name = "Hinkley Point B", constructionStartTime=3, min_running=5000, lifetime=20, down_payment=100000, ann_cost=randint(100000000, 300000000), depreciation=15, operating_cost=50000000, capacity=758, construction_time=3, carbon_emissions=50, efficiency=50)
        plant_to_invest = PowerPlant(name = "Keadby", plant_type="CCGT H Class", capacity_mw= 1200, efficiency = 0.54, pre_dev_period = 2, construction_period = 3, operating_period = 25, pre_dev_spend_years = [0.44, 0.44, 0.12], construction_spend_years = [0.4, 0.4, 0.2], pre_dev_cost_per_kw= 10, construction_cost_per_kw= 500, infrastructure = 15100, fixed_o_and_m_per_mw= 12200, variable_o_and_m = 3, insurance_cost_per_kw= 2100, connection_cost = 3300)
        self.plants.append(plant_to_invest)


    def reset_contracts(self):
        """
        Function to reset the contracts of all plants
        :return: None
        """
        for i in range(len(self.plants)):
            self.plants[i].reset_plant_contract()

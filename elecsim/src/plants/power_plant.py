"""power_plant.py: Class which represents a photovoltaic farm"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "Alexander@Kell.es"


class PowerPlant:
    def __init__(self, name, constructionStartTime, min_running, lifetime, down_payment, ann_cost, depreciation, operating_cost, capacity, construction_time, carbon_emissions, efficiency):
        # Fixed definitions

        #
        self.name = name

        # Construction details
        self.constructionStartTime = constructionStartTime


        self.min_running = min_running
        self.lifetime = lifetime
        self.down_payment = down_payment
        self.ann_cost = ann_cost
        self.depreciation = depreciation
        self.operating_cost = operating_cost
        self.capacity = capacity
        self.construction_time = construction_time
        self.efficiency = efficiency


        # Variable definitions
        self.capacity_fulfilled = 0
        self.CO2_emissions = carbon_emissions

        # Bids
        self.accepted_bids = []

    def reset_plant_contract(self):
        self.capacity_fulfilled = 0




    def __str__(self):
        ret = 'Variable Parameters: '+str(self.capacity_fulfilled) + '. Fixed Parameters: Minimum running time: ' + str(self.min_running) + ', Lifetime: ' + str(self.lifetime) + ', Down payment: ' + str(self.down_payment) + ', Annualized investment cost: ' + str(self.ann_cost) + ', Depreciation time: ' + str(self.depreciation) + ', Operating Cost: ' + str(self.operating_cost) + ', Capacity: ' + str(self.capacity) + ', Construction Time: ' + str(self.construction_time) + "."
        return ret












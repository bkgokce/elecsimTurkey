import src.scenario.scenario_data as scenario
from src.plants.plant_costs.estimate_costs.estimate_modern_power_plant_costs.predict_modern_plant_costs import PredictModernPlantParameters
from src.data_manipulation.data_modifications.extrapolation_interpolate import ExtrapolateInterpolate
from src.plants.plant_type.plant_registry import PlantRegistry
from src.scenario.scenario_data import power_plant_costs
import pandas as pd

class OldPlantCosts:
    """
    Class which takes LCOE values and type of power plants from retrospective database and predicts
    more detailed cost parameters using the same proportions as the BEIS Power Plant Cost Database.
    Specifically uses 2018 power plants from BEIS Power Plant Cost Database.
    """
    hist_costs = scenario.power_plant_historical_costs_long

    def __init__(self, year, plant_type, capacity):

        # Import historical LCOE data for power plants, and use to predict LCOE for current year based on linear
        # interpolation
        self.year = year
        self.plant_type = plant_type
        self.capacity = capacity
        # self.hist_costs = self.hist_costs[self.hist_costs.Technology == plant_type].dropna()
        self.hist_costs = self.hist_costs[self.hist_costs['Technology'].map(lambda x: x in plant_type)].dropna()

        if not all(self.hist_costs.capacity_range.str.contains(">0")):
            self.hist_costs = self.hist_costs[[pd.eval(f"{self.capacity}{j}") for j in self.hist_costs['capacity_range']]]

        self.estimated_historical_lcoe = ExtrapolateInterpolate(self.hist_costs.Year, self.hist_costs.lcoe)(year)
        self.discount_rate = self.hist_costs.Discount_rate.iloc[0]

        # self.modern_costs = power_plant_costs[power_plant_costs.Type==self.plant_type]
        self.modern_costs = power_plant_costs[power_plant_costs['Type'].map(lambda x: x in plant_type)]
        min_year = self.find_smallest_year_available()

        self.estimated_modern_plant_parameters = PredictModernPlantParameters(self.plant_type, self.capacity, min_year).parameter_estimation()

        plant_object = PlantRegistry(self.plant_type).plant_type_to_plant_object()

        self.plant = plant_object(name="Modern Plant", plant_type=self.plant_type,
                                                         capacity_mw=self.capacity, construction_year=self.year,
                                                         **self.estimated_modern_plant_parameters)
        self.modern_lcoe = self.plant.calculate_lcoe(self.discount_rate)
        self.lcoe_scaler = self.estimated_historical_lcoe / self.modern_lcoe

    def find_smallest_year_available(self):
        """
        Method which takes the modern cost BEIS database of power plants, and finds the earliest year
        that data for specified power plant type exists. For example, only returns data on Coal power plants from 2025
        as only this data is provided in the BEIS datafile
        :return: Int containing smallest year available.
        """
        available_years = self.modern_costs[['Constr_cost-Medium _2018','Constr_cost-Medium _2020', 'Constr_cost-Medium _2025']]
        columns_with_no_nan = available_years[available_years.columns[~available_years.isnull().all()]].columns
        years_with_no_nan = [s for s in columns_with_no_nan]
        years_with_no_nan = [int(s.split("_")[2]) for s in years_with_no_nan]
        minimum_year_with_data = min(years_with_no_nan)

        return minimum_year_with_data




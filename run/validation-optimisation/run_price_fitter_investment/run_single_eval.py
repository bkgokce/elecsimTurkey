

import mysql.connector
from mysql.connector import errorcode

import os.path
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))

from elecsim.model.world import World
import tracemalloc

import pandas as pd
import linecache

from elecsim.constants import ROOT_DIR
import string
from deap import algorithms
from deap import base
from deap import benchmarks
from deap.benchmarks.tools import diversity, convergence, hypervolume
from deap import creator
from deap import tools

import array
import random
import logging
logger = logging.getLogger(__name__)
import numpy as np
import numpy

from scoop import futures
import time
from pathlib import Path
project_dir = Path("__file__").resolve().parents[1]
import string
import random

"""
File name: run_GA_price_fitter
Date created: 26/07/2019
Feature: #Enter feature description here
"""

__author__ = "Alexander Kell"
__copyright__ = "Copyright 2018, Alexander Kell"
__license__ = "MIT"
__email__ = "alexander@kell.es"

pd.set_option('display.max_rows', 4000)

logging.basicConfig(level=logging.INFO)


# creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0, -1.0))
# creator.create("Individual", array.array, typecode='d',
#                fitness=creator.FitnessMin)
#
# toolbox = base.Toolbox()
#
# # Problem definition
# # Functions zdt1, zdt2, zdt3, zdt6 have bounds [0, 1]
# BOUND_LOW, BOUND_UP = 0.0, 100
#
# # Functions zdt4 has bounds x1 = [0, 1], xn = [-5, 5], with n = 2, ..., 10
# # BOUND_LOW, BOUND_UP = [0.0] + [-5.0]*9, [1.0] + [5.0]*9
#
# # Functions zdt1, zdt2, zdt3 have 30 dimensions, zdt4 and zdt6 have 10
# NDIM = 3 * 12 * 12 + 2
# # NDIM = 3 * 51 + 1
#
#
# def uniform(low, up, size=None):
#     try:
#         return [random.randint(a, b) for a, b in zip(low, up)]
#     except TypeError:
#         return [random.randint(a, b) for a, b in zip([low] * size, [up] * size)]



config = {
  'host':'elecsimresults.mysql.database.azure.com',
  'user':'alexkell@elecsimresults',
  'password':'b3rz0s4m4dr1dth3h01113s!',
  'database':'elecsim',
  'ssl_ca':'run/validation-optimisation/database/BaltimoreCyberTrustRoot.crt.pem'
}




def eval_world(individual):

    # t0 = time.time()
    # for i in range(1000):
    #     pass
    # t1 = time.time()
    #
    # time_taken = t1-t0
    # return [1], time_taken


    MARKET_TIME_SPLICES = 8
    YEARS_TO_RUN = 6
    number_of_steps = YEARS_TO_RUN * MARKET_TIME_SPLICES

    scenario_2013 = "{}/../run/validation-optimisation/scenario_file/scenario_2013.py".format(ROOT_DIR)

    world = World(initialization_year=2013, scenario_file=scenario_2013, market_time_splices=MARKET_TIME_SPLICES, data_folder="runs_2013", number_of_steps=number_of_steps, fitting_params=[individual[0], individual[1]], highest_demand=63910)
    t0 = time.time()
    for i in range(number_of_steps):
        results_df = world.step()
    t1 = time.time()

    time_taken = t1-t0

    contributed_results = results_df.filter(regex='contributed_').tail(MARKET_TIME_SPLICES)
    contributed_results *= 1/24

    # print("contributed_results: {}".format(contributed_results))
    contributed_results = contributed_results.rename(columns={'contributed_PV': "contributed_solar"})
    cluster_size = pd.Series([22.0, 30.0, 32.0, 35.0, 43.0, 53.0, 68.0, 82.0])

    # contributed_results['cluster_size'] = [22.0, 30.0, 32.0, 35.0, 43.0, 53.0, 68.0, 82.0]

    results_wa = contributed_results.apply(lambda x: np.average(x, weights=cluster_size.values)).to_frame()

    results_wa.index = results_wa.index.str.split("_").str[1].str.lower()
    # print("results_wa: {}".format(results_wa))
    offshore = results_wa.loc["offshore"].iloc[0]
    onshore = results_wa.loc["onshore"].iloc[0]
    # print("offshore: {}".format(offshore))
    results_wa.loc['wind'] = [offshore+onshore]
    # print("results_wa: {}".format(results_wa))

    electricity_mix = pd.read_csv("{}/data/processed/electricity_mix/energy_mix_historical.csv".format(ROOT_DIR))
    actual_mix_2018 = electricity_mix[electricity_mix.year == 2018]


    actual_mix_2018 = actual_mix_2018.set_index("variable")
    # print(actual_mix_2018)

    joined = actual_mix_2018[['value']].join(results_wa, how='inner')
    # print("joined: \n{}".format(joined))

    joined = joined.rename(columns={'value':'actual', 0:'simulated'})

    joined = joined.loc[~joined.index.str.contains('biomass')]

    # print("joined: \n{}".format(joined))

    joined['actual_perc'] = joined['actual']/joined['actual'].sum()
    joined['simulated_perc'] = joined['simulated']/joined['simulated'].sum()

    print("joined: \n{}".format(joined))

    total_difference_col = joined['actual_perc'] - joined['simulated_perc']
    # print(total_difference_col)
    total_difference = total_difference_col.abs().sum()
    # print("max_demand : dif: {} :x {}".format(individual, total_difference))
    # print(joined.simulated)
    print("returns: {}, {}, {}".format([total_difference], time_taken, joined.simulated))
    return [total_difference], time_taken, joined.simulated


# for i in np.linspace(62244, 66326, num=50):
#     eval_world(i)

eval_world([0.002547, -13.374101])
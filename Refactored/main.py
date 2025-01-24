from Simulation import Simulation
from Matrix import PMatrix
from Backtrack_Strategy import BackTrack_Strategy
from Best_Visible_Strategy import BestVisibleSpotStrategy
from n_of_x_Strategy import n_of_x_Strategy
from Park_After_N_Stategy import Park_After_N_Strategy
from Park_First_Available_Spot import ParkFirstAvailableSpot
from SimpleVis import SimpleVis
from Bernouli_ProbDist import Bernouli_ProbDist
from Bernouli_ProbDist_Old import Bernouli_Probdist_Old
from Dist_Dependent_ProbDist import distDependentProb
from Linear_probDist import Linear_PropDist
import pandas as pd
import pandas

nrOfSpots = 100
nrOfTrials = 1000
# dist = Linear_PropDist(nrOfSpots)
dist = distDependentProb(nrOfSpots, 30)
vis = SimpleVis(visionRange=1)
matrix = PMatrix(nrOfSpots, dist)
drivingSpeed = 1
walkingSpeed = 2
N = round(nrOfSpots * 0.8)
density_threshold = 0.6
# strats = [n_of_x_Strategy(vis, 0.2, N), n_of_x_Strategy(vis, 0.4, N), n_of_x_Strategy(vis, 0.6, N), n_of_x_Strategy(vis, 0.8, N), n_of_x_Strategy(vis, 0.9, N)]
# strats = [Park_After_N_Strategy(vis, nrOfSpots * 0.6), Park_After_N_Strategy(vis, nrOfSpots * 0.7), Park_After_N_Strategy(vis, nrOfSpots * 0.8), Park_After_N_Strategy(vis, nrOfSpots * 0.9), Park_After_N_Strategy(vis, nrOfSpots)]
# strats = [ParkFirstAvailableSpot(vis), BackTrack_Strategy(vis), BestVisibleSpotStrategy(vis), n_of_x_Strategy(vis, density_threshold, N), Park_After_N_Strategy(vis, N)]
# strats = [ParkFirstAvailableSpot(vis), BackTrack_Strategy(vis), BestVisibleSpotStrategy(vis), n_of_x_Strategy(vis, 0.2, 0.8 * nrOfSpots), Park_After_N_Strategy(vis, 0.8 * nrOfSpots)]
# strats = [Park_After_N_Strategy(vis, 66), Park_After_N_Strategy(vis, 80)]
# strats = [ParkFirstAvailableSpot(vis), BackTrack_Strategy(vis), BestVisibleSpotStrategy(vis)]
strats = [n_of_x_Strategy(vis, 0.2, N), BackTrack_Strategy(vis)]
results = {}

#Generate dictionary to append results to.
for count, strat in enumerate(strats):
    results[count] = []

print("Running " + str(nrOfTrials) + " simulation with " + str(nrOfSpots) + " parking spots.")

#Run simulations
# for i in range(nrOfTrials):
#     matrix.regenarateMatrix()
#     for strat in strats:
#         strat_name = type(strat).__name__
#         result = Simulation(strat, matrix, verbose=False, timeOut=10000).getInfo()['score']
#         if result is None:
#             print("none result")
#             quit()
#         results[strat_name].append(result)
#         strat.resetStrat()
# print(pd.DataFrame(results))

# test a spread of parameters
df_expectation_1 = pd.DataFrame()
df_std_1 = pd.DataFrame()

for count, strat in enumerate(strats):
    df_expectation_1[count] = pd.Series(dtype=float)
    df_std_1[count] = pd.Series(dtype=float)

df = pandas.DataFrame()
for count, strat in enumerate(strats):
    df[count] = pd.Series(dtype=float)
    df[count] = pd.Series(dtype=float)

#Bernouli population
for b in range(100):
    matrix.setDist(Bernouli_Probdist_Old(nrOfSpots, b))
    for i in range(nrOfTrials):
        matrix.regenarateMatrix()
        # Simulation(strat, matrix, verbose=False).print_status(0, 0)
        for count, strat in enumerate(strats):
            df.at[i, count] = Simulation(strat, matrix, verbose=False, drivingSpeed=drivingSpeed, walkingSpeed=walkingSpeed).getInfo()['score']
            strat.resetStrat()
        # print(df)
    df_expectation_1.loc[b] = df.describe().loc['mean']
    df_std_1.loc[b] = df.describe().loc['std']
    #Clear dataframe
    df = df.iloc[0:0]



df_expectation_2 = pd.DataFrame()
df_std_2 = pd.DataFrame()

for count, strat in enumerate(strats):
    df_expectation_2[count] = pd.Series(dtype=float)
    df_std_2[count] = pd.Series(dtype=float)

df = pandas.DataFrame()
for count, strat in enumerate(strats):
    df[count] = pd.Series(dtype=float)
    df[count] = pd.Series(dtype=float)

#Exponential population
for b in range(100):
    matrix.setDist(distDependentProb(nrOfSpots, b))
    for i in range(nrOfTrials):
        matrix.regenarateMatrix()
        for count, strat in enumerate(strats):
            df.at[i, count] = Simulation(strat, matrix, verbose=False, drivingSpeed=drivingSpeed, walkingSpeed=walkingSpeed).getInfo()['score']
            strat.resetStrat()
        # print(df)
    df_expectation_2.loc[b] = df.describe().loc['mean']
    df_std_2.loc[b] = df.describe().loc['std']
    #Clear dataframe
    df = df.iloc[0:0]

import matplotlib.pyplot as plt


B= [x/100 for x in range(100)]

fig, axs = plt.subplots(1, len(strats), sharey=True, figsize=(5 * len(strats),5))

axs[0].set_ylabel("Average parking time")
for count, strat in enumerate(strats):

    axs[count].scatter(B, df_expectation_1[count], label="distance independent")
    axs[count].scatter(B, df_expectation_2[count], label="distance dependent")
    axs[count].set_title(strat.getName())
    axs[count].set_xlabel("busyness, b")
    if (type(strat).__name__ == "n_of_x_Strategy"):
        axs[count].legend(loc="best", title=f"Skipping first {strat.n} spots\nThreshold = {strat.threshold}")
    elif (type(strat).__name__ == "Park_After_N_Strategy"):
        axs[count].legend(loc="best", title=f"Skipping first {strat.n} spots")
    else:
        axs[count].legend(loc="best")

plt.tight_layout()

# Show the plot
plt.show()


fig, axs = plt.subplots(1, len(strats), sharey=True, figsize=(5 * len(strats),5))

axs[0].set_ylabel("Standard deviation")
for count, strat in enumerate(strats):

    axs[count].scatter(B, df_std_1[count], label="distance independent")
    axs[count].scatter(B, df_std_2[count], label="distance dependent")
    axs[count].set_title(strat.getName())
    axs[count].set_xlabel("busyness, b")
    if (type(strat).__name__ == "n_of_x_Strategy"):
        axs[count].legend(loc="best", title=f"Skipping first {strat.n} spots\nThreshold = {strat.threshold}")
    elif (type(strat).__name__ == "Park_After_N_Strategy"):
        axs[count].legend(loc="best", title=f"Skipping first {strat.n} spots")
    else:
        axs[count].legend(loc="best")


plt.tight_layout()

# Show the plot
plt.show()

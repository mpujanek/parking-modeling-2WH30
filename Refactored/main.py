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
nrOfTrials = 100
# dist = Linear_PropDist(nrOfSpots)
dist = distDependentProb(nrOfSpots, 30)
vis = SimpleVis(visionRange=1)
matrix = PMatrix(nrOfSpots, dist)
strats = [BackTrack_Strategy(vis), BestVisibleSpotStrategy(vis), n_of_x_Strategy(vis, 1, nrOfSpots/3),
           Park_After_N_Strategy(vis, nrOfSpots/3), ParkFirstAvailableSpot(vis)]
results = {}

#Generate dictionary to append results to.
for strat in strats:
    strat_name = type(strat).__name__
    results[strat_name] = []

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

# test a spread of parameters
df_expectation_1 = pd.DataFrame()
df_std_1 = pd.DataFrame()

for strat in strats:
    df_expectation_1[type(strat).__name__] = pd.Series(dtype=float)
    df_std_1[type(strat).__name__] = pd.Series(dtype=float)

df = pandas.DataFrame()
for strat in strats:
    df[type(strat).__name__] = pd.Series(dtype=float)
    df[type(strat).__name__] = pd.Series(dtype=float)

#Bernouli population
for b in range(100):
    matrix.setDist(Bernouli_Probdist_Old(nrOfSpots, b))
    for i in range(nrOfTrials):
        matrix.regenarateMatrix()
        for strat in strats:
            df.at[i, type(strat).__name__] = Simulation(strat, matrix, verbose=False).getInfo()['score']
            strat.resetStrat()
        # print(df)
    df_expectation_1.loc[b] = df.describe().loc['mean']
    df_std_1.loc[b] = df.describe().loc['std']
    #Clear dataframe
    df = df.iloc[0:0]

df_expectation_2 = pd.DataFrame()
df_std_2 = pd.DataFrame()

for strat in strats:
    df_expectation_2[type(strat).__name__] = pd.Series(dtype=float)
    df_std_2[type(strat).__name__] = pd.Series(dtype=float)

df = pandas.DataFrame()
for strat in strats:
    df[type(strat).__name__] = pd.Series(dtype=float)
    df[type(strat).__name__] = pd.Series(dtype=float)

#Exponential population
for b in range(100):
    matrix.setDist(distDependentProb(nrOfSpots, b))
    for i in range(nrOfTrials):
        matrix.regenarateMatrix()
        for strat in strats:
            df.at[i, type(strat).__name__] = Simulation(strat, matrix, verbose=False).getInfo()['score']
            strat.resetStrat()
        # print(df)
    df_expectation_2.loc[b] = df.describe().loc['mean']
    df_std_2.loc[b] = df.describe().loc['std']
    #Clear dataframe
    df = df.iloc[0:0]


import matplotlib.pyplot as plt

B=range(100)

fig, axs = plt.subplots(1, 5, figsize=(15, 5), sharey=True)

print(df_std_1)
print(df_expectation_1)

# # first available spot strategy
# axs[0].scatter(B, df_std_1["ParkFirstAvailableSpot"], label="distance independent")
# axs[0].scatter(B, df_std_2["ParkFirstAvailableSpot"], label="distance dependent")
# axs[0].set_title("First available spot")
# axs[0].set_xlabel("busyness, b")
# axs[0].legend(loc="best")
# axs[0].set_ylabel("Variance of total time, V[T^t]")

# # greedy strategy
# axs[1].scatter(B, df_std_1["BackTrack_Strategy"], label="distance independent")
# axs[1].scatter(B, df_std_2["BackTrack_Strategy"], label="distance dependent")
# axs[1].set_title("Greedy strategy")
# axs[1].set_xlabel("busyness, b")
# axs[1].legend(loc="best")
# #axs[1].set_ylabel("E[T^t]")

# # best visible spot strategy
# axs[2].scatter(B, df_std_1["BestVisibleSpotStrategy"], label="distance independent")
# axs[2].scatter(B, df_std_2["BestVisibleSpotStrategy"], label="distance dependent")
# axs[2].set_title("Best visible spot")
# axs[2].set_xlabel("busyness, b")
# axs[2].legend(loc="best")
#axs[2].set_ylabel("E[T^t]")
#axs[2].set_ylim(-10, 10)  # Limit y-axis for better visibility

# first available spot strategy
axs[0].scatter(B, df_expectation_1["ParkFirstAvailableSpot"], label="distance independent")
axs[0].scatter(B, df_expectation_2["ParkFirstAvailableSpot"], label="distance dependent")
axs[0].set_title("First available spot")
axs[0].set_xlabel("busyness, b")
axs[0].legend(loc="best")
axs[0].set_ylabel("Variance of total time, V[T^t]")

# greedy strategy
axs[1].scatter(B, df_expectation_1["BackTrack_Strategy"], label="distance independent")
axs[1].scatter(B, df_expectation_2["BackTrack_Strategy"], label="distance dependent")
axs[1].set_title("Greedy strategy")
axs[1].set_xlabel("busyness, b")
axs[1].legend(loc="best")
#axs[1].set_ylabel("E[T^t]")

# best visible spot strategy
axs[2].scatter(B, df_expectation_1["BestVisibleSpotStrategy"], label="distance independent")
axs[2].scatter(B, df_expectation_2["BestVisibleSpotStrategy"], label="distance dependent")
axs[2].set_title("Best visible spot")
axs[2].set_xlabel("busyness, b")
axs[2].legend(loc="best")

axs[3].scatter(B, df_expectation_1["n_of_x_Strategy"], label="distance independent")
axs[3].scatter(B, df_expectation_2["n_of_x_Strategy"], label="distance dependent")
axs[3].set_title("n_of_x_Strategy")
axs[3].set_xlabel("busyness, b")
axs[3].legend(loc="best")

axs[4].scatter(B, df_expectation_1["Park_After_N_Strategy"], label="distance independent")
axs[4].scatter(B, df_expectation_2["Park_After_N_Strategy"], label="distance dependent")
axs[4].set_title("Park_After_N_Strategy")
axs[4].set_xlabel("busyness, b")
axs[4].legend(loc="best")

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()

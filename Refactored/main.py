from Simulation import Simulation
from Matrix import PMatrix
from Backtrack_Strategy import BackTrack_Strategy
from Best_Visible_Strategy import BestVisibleSpotStrategy
from n_of_x_Strategy import n_of_x_Strategy
from Park_After_N_Stategy import Park_After_N_Strategy
from Park_First_Available_Spot import ParkFirstAvailableSpot
from SimpleVis import SimpleVis
from Bernouli_ProbDist import Bernouli_ProbDist
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
strats = [BackTrack_Strategy(vis), BestVisibleSpotStrategy(vis), n_of_x_Strategy(vis, 0.6, nrOfSpots/3),
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

#bernouli
df_expectation_1 = pandas.DataFrame(results)
df_std_1 = pandas.DataFrame(results)
for b in range(100):
    for i in range(nrOfTrials):
        dist = Bernouli_ProbDist(nrOfSpots)
        matrix.regenarateMatrix()
        for strat in strats:
            strat_name = type(strat).__name__
            result = Simulation(strat, matrix, verbose=False, timeOut=10000).getInfo()['score']
            if result is None:
                print("none result")
                quit()
            results[strat_name].append(result)
            strat.resetStrat()

df = pd.DataFrame(results)
for i in range(100):
    df_expectation_1.loc[i] = df.loc[i * nrOfTrials : (i + 1) * nrOfTrials - 1].mean()
    df_std_1.loc[i] = df.loc[i * nrOfTrials : (i + 1) * nrOfTrials - 1].std()



#Exponential
results = {}

#Generate dictionary to append results to.
for strat in strats:
    strat_name = type(strat).__name__
    results[strat_name] = []

df_expectation_2 = pandas.DataFrame(results)
df_std_2 = pandas.DataFrame(results)
for b in range(100):
    for i in range(nrOfTrials):
        dist = distDependentProb(nrOfSpots, b)
        matrix.regenarateMatrix()
        for strat in strats:
            strat_name = type(strat).__name__
            result = Simulation(strat, matrix, verbose=False, timeOut=10000).getInfo()['score']
            if result is None:
                print("none result")
                quit()
            results[strat_name].append(result)
            strat.resetStrat()
    
df = pd.DataFrame(results)
for i in range(100):
    df_expectation_2.loc[i] = df.loc[i * nrOfTrials : (i + 1) * nrOfTrials - 1].mean()
    df_std_2.loc[i] = df.loc[i * nrOfTrials : (i + 1) * nrOfTrials - 1].std()


import matplotlib.pyplot as plt

B=range(100)

fig, axs = plt.subplots(1, 3, figsize=(15, 5), sharey=True)

# first available spot strategy
axs[0].scatter(B, df_std_1[ParkFirstAvailableSpot.__name__], label="distance independent")
axs[0].scatter(B, df_std_2[ParkFirstAvailableSpot.__name__], label="distance dependent")
axs[0].set_title("First available spot")
axs[0].set_xlabel("busyness, b")
axs[0].legend(loc="best")
axs[0].set_ylabel("Variance of total time, V[T^t]")

# greedy strategy
axs[1].scatter(B, df_std_1[BackTrack_Strategy.__name__], label="distance independent")
axs[1].scatter(B, df_std_2[BackTrack_Strategy.__name__], label="distance dependent")
axs[1].set_title("Greedy strategy")
axs[1].set_xlabel("busyness, b")
axs[1].legend(loc="best")
#axs[1].set_ylabel("E[T^t]")

# best visible spot strategy
axs[2].scatter(B, df_std_1[BestVisibleSpotStrategy.__name__], label="distance independent")
axs[2].scatter(B, df_std_2[BestVisibleSpotStrategy.__name__], label="distance dependent")
axs[2].set_title("Best visible spot")
axs[2].set_xlabel("busyness, b")
axs[2].legend(loc="best")
#axs[2].set_ylabel("E[T^t]")
#axs[2].set_ylim(-10, 10)  # Limit y-axis for better visibility

# Adjust spacing between subplots
plt.tight_layout()

# Show the plot
plt.show()

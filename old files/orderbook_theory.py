'''
order book theory

IGNORE THIS FILE
'''
import random, time
import numpy as np
import matplotlib.pyplot as plt

distance = np.array([20,30,40,50])
small_trial_1 = np.array([1.06, 1.25, 1.59, 1.73])
small_trial_2 = np.array([0.72,1.05,1.22,1.36])
big_trial_1 = np.array([1.1,1.46,1.55,1.73])
big_trial_2 = np.array([0.86,1.09,1.37,1.47])

# plt.set_title('Small Glider Trial 1 Best Fit Line Plot')

# plt.plot(distance, small_trial_1, '.r', ms=10, label='Trial 1')
# plt.plot(distance, small_trial_2, '.g', ms=10, label='Trial 2')





# print(np.polyfit(distance,small_trial_1,1)[9])

# plt.title('Big Glider (Trial 1) Best Fit Line PLot')

plt.subplot(1,2,1)
plt.plot(distance, small_trial_1, '.r', ms=10, label='Trial 1')
coeff = np.polyfit(distance,small_trial_1,1)
poly_1dfn = np.poly1d(coeff)
plt.plot(distance, poly_1dfn(distance), 'k')

plt.ylabel('Time (s)')
plt.xlabel('Distance (cm)')
plt.legend()
print(coeff[1])

plt.subplot(1,2,2)
plt.plot(distance, small_trial_2, '.g', ms=10, label='Trial 2')
coeff = np.polyfit(distance,small_trial_2,1)
poly_1dfn = np.poly1d(coeff)
plt.plot(distance, poly_1dfn(distance), 'k')


plt.xlabel('Distance (cm)')
plt.legend()



plt.show()


'''
time_horizon = 100
delta_t = 1
# mu = 0.05 / 100 # drift (5% annual return)
sigma = 0.01 # volatility
initial_price = 100

for i in range(100):
    x = np.linspace(0, time_horizon, time_horizon)
    y = np.zeros(time_horizon)
    y[0] = initial_price
    mu = 0.05 / len(y)

    for i in range(1, time_horizon):
        y[i] = y[i-1] * np.exp((mu - 0.5 * sigma ** 2) * delta_t + sigma * np.sqrt(delta_t) * np.random.normal(0,1))

    plt.plot(x,y)

plt.show()
'''
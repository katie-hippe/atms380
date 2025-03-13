## KATIE HIPPE 
## ATM S 380
## HOMEWORK 2
## January 31, 2025

import numpy as np
import matplotlib.pyplot as plt
import scipy.io as io

## (a)
print("(a)")

# load in the hadcrut5 
hadcrut5full = io.loadmat('HadCRUT5.mat', squeeze_me = True)
t_had = hadcrut5full['T_HadCRUT5']

# define function for looping through our differential equations 
def twolayerEMB (t_init,t_final, delta_t, T_0, TO_0, C, CO, Rf, l, g):
    curr_T = T_0
    curr_TO = TO_0

    T = [curr_T]
    TO = [curr_TO]

    for t in range(t_init, t_final + 1):
        # delta t = 3.154e7 lazy hardcoding
        next_T = curr_T + (3.1536e7 / C) * (Rf[t - t_init] + l * curr_T - g * (curr_T - curr_TO))
        next_TO = curr_TO + (3.1537e7 / CO) * g * (curr_T - curr_TO)

        curr_T = next_T
        curr_TO = next_TO 

        T.append(curr_T)
        TO.append(curr_TO)

    return T, TO

# set up our inputs 
T_0, TO_0 = 0,0
t_init = 1
t_final = 500
deltat = 1
Rf = np.full((t_final+1), 3.9) # make an array for ease down the line 
C = 1025 * 3850 * 70 # lazy hard-coding
CO = 1025 * 3850 * 1100
l = -1
g = .7

# run our model over 500 years 
T, TO = twolayerEMB(t_init, t_final, 1, T_0, TO_0, C, CO, Rf, l, g)

# plotting function (for laziness purposes)

def plotT(t_init, t_final, deltat, T, TO, historical, title):
    # axis for plotting purposes
    axis = np.arange(t_init, t_final+2, deltat)

    # plot stuff!
    plt.plot(axis,T, label="Surface Temperature Change")
    plt.plot(axis, TO, label="Deep Ocean Change")
    if historical:
        plt.plot(np.arange(1850,2023, 1), t_had, label="HadCRUT5") # hard-coded in bc i'm lazy 
    plt.xlabel("Year", fontsize = 15)
    plt.ylabel("Temperature Change", fontsize = 15)
    plt.legend(loc="upper left")
    plt.title(title)
    plt.show()

# plot our T!
plotT(t_init, t_final, deltat, T, TO, False, '(a)')

# (i)
print("(i)")
print("The equilibrium climate sensitivity is 3.9K.")
print("(ii)")
print("The fraction that's reached after 20 years is", T[20] / 3.9)
print("(iii)")
print("The fraction that's reached after 500 years is", T[500] / 3.9)


# (b)
print("\n(b)")

# read in the R forcing data stuff 
forcingdata = io.loadmat('HistoricalForcings.mat', squeeze_me = True)
year = forcingdata['year']
RCO2 = forcingdata['RCO2']
RCH4 = forcingdata['RCH4']
RN2O = forcingdata['RN2O']
Rother = forcingdata['Rother']
Raerosol = forcingdata['Raerosol']
Rvolcanic = forcingdata['Rvolcanic']

# fiddle with lambda 
l = -1.4

t_init, t_final = 1765, 2100
R = RCO2 + RCH4 + RN2O + Raerosol + Rvolcanic + Rother
T, TO = twolayerEMB(t_init, t_final, 1, T_0, TO_0, C, CO, R, l, g)

plotT(t_init, t_final, deltat, T, TO, True, '(b)')

# save first tuned model
T_b = T

print("By the end of the 21st century, I predict about ", T[-1], "degrees of warming.")
b_ECS = 3.9 / -l
print("This model has an ECS of", b_ECS, "K.")


# moving on 
# (c) 

print('\n(c)')
R = [RCO2, RCH4, Raerosol, Rvolcanic, Rother]
titles = ['RCO2', 'RCH4', 'Raerosol', 'Rvolcanic', 'Rother']

for i in range(len(R)):
    currR = R[i]
    title = titles[i]
    T, TO = twolayerEMB(t_init, t_final, 1, T_0, TO_0, C, CO, currR, l, g)
    plotT(t_init, t_final, deltat, T, TO, True, title)

    # print out answers to the question 
    contribution = np.mean(T[2010-t_init:2019 + 1-t_init]) - np.mean(T[1850-t_init:1900 + 1 - t_init])
    print(title, 'contributes', contribution, 'K of warming.')

print('These values match well in terms of direction and simple relative magnitude',
      'but aren\'t that accurate to exact numbers.')

# (d)
print('\n(d)')

# grab the other column we want
Raerosol_strong = forcingdata['Raerosol_strong']
R = RCO2 + RCH4 + RN2O + Raerosol_strong + Rvolcanic + Rother

# fiddle with lambda 
l = -1.1
T, TO = twolayerEMB(t_init, t_final, 1, T_0, TO_0, C, CO, R, l, g)

plotT(t_init, t_final, deltat, T, TO, True, '(d)')

# save second tuned model 
T_d = T

print("By the end of the 21st century, I predict about ", T[-1], "degrees of warming.")
d_ECS = 3.9 / -l
print("This model has an ECS of", d_ECS, "K.")


# (e)
print('\n(e)')

# grab the other column we want
Raerosol_weak = forcingdata['Raerosol_weak']
R = RCO2 + RCH4 + RN2O + Raerosol_weak + Rvolcanic + Rother

# fiddle with lambda
l = -1.9

T, TO = twolayerEMB(t_init, t_final, 1, T_0, TO_0, C, CO, R, l, g)

plotT(t_init, t_final, deltat, T, TO, True, '(e)')

# save second tuned model 
T_e = T

print("By the end of the 21st century, I predict about ", T[-1], "degrees of warming.")
e_ECS = 3.9 / -l
print("This model has an ECS of", e_ECS, "K.")


# (f)
print('\n(f)')

# plot of ECS against projected 2100 warming 
ECS = [b_ECS, d_ECS, e_ECS]
warm_2100 = [T_b[-1], T_d[-1],T_e[-1]]

plt.scatter(ECS, warm_2100)
plt.title('2100 Projected Warming vs ECS')
plt.xlabel('Model ECS')
plt.ylabel('Model Projected Warming in 2100')
plt.show()


# plot of ECS against aerosol radiative forcing in 2006
aero_2006 = [Raerosol[242], Raerosol_strong[242], Raerosol_weak[242]]
plt.scatter(aero_2006, ECS)
plt.title('ECS vs Aerosol Radiative Forcing')
plt.xlabel('Radiative Forcing in 2006')
plt.ylabel('Model ECS')
plt.show()

print('Proected warming is proportional to ECS. The higher the ECS, the more sensitive')
print('the model is to change and the higher the projected warming will be.')
print('ECS is inversely proportional to aerosol radiative forcing. Aerosols cool the')
print('atmosphere, so the stronger the aerosols, the weaker warming and lower the ECS.')

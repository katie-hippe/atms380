## KATIE HIPPE 
## ATM S 380
## HOMEWORK 1
## January 22, 2025

## PROBLEM 1

# T_s is earth's global surface temperature, T_a is atmospheric layer temp
S_0 = 1367
sigma = 5.67e-08
alpha_0 = 0.3
epsilon_0 = 0.77

def Ts(alpha, S_0, sigma, epsilon):
    Ts = ((1-alpha)*(S_0/4) / (sigma*(1-epsilon / 2)))**(1/4)
    return Ts

def Ta(Ts):
    return Ts / (2**(1/4))


# a 


Ts_0 = Ts(alpha_0, S_0, sigma, epsilon_0)
Ta_0 = Ta(Ts_0)

print('(a)')
print('The values of T_s and T_a for today\'s climate are: T_s = ',
       Ts_0, 'and T_a = ', Ta_0)


# b


# consider delta R_f
def deltaRf(deltae, sigma, Ts, Ta):
    return deltae*(sigma*Ts**4 - sigma*Ta**4)

deltae = 0.02
deltaRfb = deltaRf(deltae, sigma, Ts_0, Ta_0)

print('\n(b)')
print('The change in radiative forcing is: ', deltaRfb)


# c


epsilon_1 = .79
Ts_c = Ts(alpha_0, S_0, sigma, epsilon_1)

print('\n(c)')
print('The ECS for this model is: ', Ts_c - Ts_0, 
      '. This is much smaller than the estimated ECS of 2-5 because of the',
       ' lack of feedback loops that would end up increasing the climate sensitivity.')


# d

print('\n(d)')

def lambda_fb(epsilon, sigma, Ts):
    return -4 * (1 - (epsilon / 2))*sigma*Ts**3

lambda_d = lambda_fb(epsilon_0, sigma, Ts_0)
print('The value of lambda for this model is:', lambda_d)

deltaTs = - deltaRfb / lambda_d
print('The value of delta Ts is:', deltaTs)
print('This value is very similar to the delta T as calculated above in part (c)!')


## PROBLEM 2


def alpha(a0, aprime, Ts, Ts_0):
    return a0 + aprime*(Ts - Ts_0)

def epsilon(e0, eprime, Ts, Ts_0):
    return e0 + eprime*(Ts - Ts_0)

def Ts_iterative(Ts, Ts_0, S_0, sigma):
    return ((1-alpha(alpha_0, aprime, Ts, Ts_0))*(S_0/4)/
            (sigma*(1-epsilon(epsilon_1, eprime, Ts, Ts_0)/2)))**(1/4)

aprime = -1.18e-3
eprime = 8.25e-3


# e 

print('\n(e)')

diff = 1
Ts_curr = Ts_iterative(Ts_0, Ts_0, S_0, sigma)
while diff > .01:
    Ts_next = Ts_iterative(Ts_curr, Ts_0, S_0, sigma)
    diff = Ts_next - Ts_curr
    Ts_curr = Ts_next

print('Our final value of Ts is:', Ts_curr)
print('The delta t is:', Ts_curr - Ts_0)
print('This delta t is now within our desired range of 2-5K.')


# f

print('\n(f)')

def lambda_0(epsilon_0, sigma, Ts):
    return -4 * (1-epsilon_0/2)*sigma*Ts**3

def lambda_alpha(aprime, S_0):
    return -aprime * S_0 / 4

def lambda_epsilon(eprime, sigma, Ts):
    return .5*eprime * sigma*Ts**4

l_0 = lambda_0(epsilon_0, sigma, Ts_0)
l_a = lambda_alpha(aprime, S_0)
l_e = lambda_epsilon(eprime, sigma, Ts_0)

l = l_0 + l_a + l_e

deltaTs = - deltaRfb / l
print('Our detla Ts is now:', deltaTs)
print('This is slightly smaller than the delta t as calculated in (e).')


# g

print('\n(g)')

aprime = -2.36e-3
l_a = lambda_alpha(aprime, S_0)
l = l_0 + l_a + l_e
deltaTs = -deltaRfb / l
print('Under a\' = ', aprime, ':')
print('   lambda_alpha is now:', l_a)
print('   lambda is now:', l)
print('   delta Ts is now:', deltaTs)

aprime = 0
l_a = lambda_alpha(aprime, S_0)
l = l_0 + l_a + l_e
deltaTs = -deltaRfb / l
print('Under a\' = ', aprime, ':')
print('   lambda_alpha is now:', l_a)
print('   lambda is now:', l)
print('   delta Ts is now:', deltaTs)

print('These are still within range of 2-5K!')


# h 


print('\n(h)')
print('This range is not symmetric about the best estimate because',
      'we are able to get a lower bound much more easily than an upper bound',
      'due to the 1/lambda distribution to calculate delta Ts. Our values from',
      'parts (e)-(g) reflect this skewed distribution as more of the values are',
      'close to 3 while there is one value further away greater than 4.')
# the range is not symmetric about the best estimate because we are 
# able to get a lower bound more easily than an upper bound because 
# of the 1/lambda distribution for delta Ts
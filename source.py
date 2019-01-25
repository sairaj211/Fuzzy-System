import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt

x_temp = np.arange(0, 40, 1)
x_moist = np.arange(0, 60, 1)
x_water = np.arange(0, 60, 1)
numerator = 0
denominator = 0


def membership(i,input1):
    
    global side
   
    if (i[0] == i[1]):
        if input1 < i[0] or input1 > i[2]:
            return 0
        elif input1 == i[2]:
            return 0
        elif input1 == i[1] or input1 == i[0]:
            return 1
        else :
            return ( (i[2] - input1) / (i[2] - i[0]) )
        
    elif (i[1] == i[2]):
        if input1 < i[0] or input1 > i[2]:
            return 0
        elif input1 == i[2]:
            return 1
        else :
            return ( (input1 - i[0]) / (i[1] - i[0]) )
     
    else:
        if input1 < i[0] or input1 > i[2] or input1 == i[0]:
            return 0
        elif input1 == i[1]:
            return 1
        elif input1 > i[0] and input1 <= i[1]:
            return ( (input1 - i[0]) / (i[1] - i[0]) )
        elif input1 > i[1] and input1 <= i[2]:
            return ( (i[2] - input1) / (i[2] - i[1]) )
               
       
    
# 9 firing levels      
def rules(i,j):

    if i == 0 and j == 0:
        return 0
    elif i == 0 and j == 1:
        return 0
    elif i == 0 and j == 2:
        return 0
    elif i == 1 and j == 0:
        return 1
    elif i == 1 and j == 1:
        return 1
    elif i == 1 and j == 2:
        return 1
    elif i == 2 and j == 0:
        return 2
    elif i == 2 and j == 1:
        return 2
    elif i == 2 and j == 2:
        return 2
    
antecedent1 = [ [0,0,20], [15,25,30], [28,40,40]]
antecedent2 = [ [0,0,30], [20,30,40], [35,60,60]]

consequence = [ [0,15,25], [20,30,40], [35,45,60]]


if __name__== "__main__":
    
    temperature = int(input("Input 1 temperature : "))
    while(temperature > 40):
        temperature = int(input("Please enter temperature upto 40 degrees : "))
    
    moisture = int(input("Input 2 moisture level : "))
    while(moisture > 60):
        moisture = int(input("Please enter moisture level between 0 - 60 psi : "))
        
   
    temp=[]
    moist=[]
    alphas = []
    z_values = []
    
    for i in range(0,3):

        temp.append( membership(antecedent1[i],temperature))

        for j in range(0,3):
            moist.append ( membership(antecedent2[j],moisture))

            alphas.append(min(temp[i],moist[j]))
            k = rules(i,j)
            
            alpha = ( (consequence[k][2]) - (consequence[k][0]) ) / ( (antecedent1[i][2]) - (antecedent1[i][0]) )
            
            beta = ( (consequence[k][2]) - (consequence[k][0]) ) / ( (antecedent2[i][2]) - (antecedent2[i][0]) )
     
            constant = consequence[k][1] - ( alpha * antecedent1[i][1]) - (beta * antecedent2[j][1])

            x = (alpha*float(temperature)) + (beta*float(moisture)) + constant
            z_values.append(x)

        
    for i in range(len(z_values)):
        numerator += (z_values[i] * alphas[i])
        denominator += alphas[i]
        
    COG = numerator / denominator
    
    water_activation = 1 

        # Generate fuzzy membership functions
    temp_lo = fuzz.trimf(x_temp, [0, 0, 20])
    temp_md = fuzz.trimf(x_temp, [15, 25, 30])
    temp_hi = fuzz.trimf(x_temp, [28, 40, 40])
    moist_lo = fuzz.trimf(x_moist, [0, 0, 30])
    moist_md = fuzz.trimf(x_moist, [20, 30, 40])
    moist_hi = fuzz.trimf(x_moist, [35, 60, 60])
    water_lo = fuzz.trimf(x_water, [0, 15, 25])
    water_md = fuzz.trimf(x_water, [20, 30, 40])
    water_hi = fuzz.trimf(x_water, [35, 45, 60])
    
    # Visualize these universes and membership functions
    fig, (ax0, ax1, ax2) = plt.subplots(nrows=3, figsize=(8, 9))
    ax0.plot(x_temp, temp_lo, 'b', linewidth=1.5, label='Low')
    ax0.plot(x_temp, temp_md, 'g', linewidth=1.5, label='Medium')
    ax0.plot(x_temp, temp_hi, 'r', linewidth=1.5, label='High')
    ax0.set_title('Temperature')
    ax0.legend()
    ax1.plot(x_moist, moist_lo, 'b', linewidth=1.5, label='Low')
    ax1.plot(x_moist, moist_md, 'g', linewidth=1.5, label='Medium')
    ax1.plot(x_moist, moist_hi, 'r', linewidth=1.5, label='High')
    ax1.set_title('Moisture Level')
    ax1.legend()
    ax2.plot(x_water, water_lo, 'b', linewidth=1.5, label='Low')
    ax2.plot(x_water, water_md, 'g', linewidth=1.5, label='Medium')
    ax2.plot(x_water, water_hi, 'r', linewidth=1.5, label='High')
    ax2.set_title('Water Pressure')
    ax2.legend()
    # Turn off top/right axes
    for ax in (ax0, ax1, ax2):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        
    plt.tight_layout()
    plt.show()
    
    fig, ax0 = plt.subplots(figsize=(8, 3))
    ax0.plot(x_water, water_lo, 'b', linewidth=0.5, linestyle='--', )
    ax0.plot(x_water, water_md, 'g', linewidth=0.5, linestyle='--')
    ax0.plot(x_water, water_hi, 'r', linewidth=0.5, linestyle='--')
    ax0.plot([COG, COG], [0, water_activation], 'k', linewidth=1.5, alpha=0.9)
    ax0.set_title('Output using TS (line)')
    
    # Turn off top/right axes
    for ax in (ax0,):
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
    plt.tight_layout()
    plt.show()
    
    
    print("COG of system is = ", COG)

    

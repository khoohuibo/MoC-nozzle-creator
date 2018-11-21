import math as m
import numpy as np
import pandas as pd
from bisect import bisect_left
import matplotlib.pyplot as plt
from scipy import interpolate

gamma = 1.2
list_counter = []
list_M = []
list_angle_M = []
list_PMV = []
list_PMV_deg = []
list_final_ratio = []
list_final_ratio_1_4 = []


list_M_MoC = []
list_angle_M_MoC = []
PMV_deg_MoC = []
list_R_minus = []
list_R_positive = []
turning_angles_init = []
final_turning_angles = []
turn_minus_mach_angle = []
turn_plus_mach_angle = []
x_points = []
y_points =[]
point_list = ['a','b','c','d',1,2,3,4,5,6,7,8,9,10,11,12,13,14]

def max_turn_angle(mach_number):
    if mach_number in list_M:
        pos = list_M.index(mach_number)
        max_turn = list_PMV_deg[pos]/2
        print(max_turn)
        return float(max_turn)
    else:
        print("Error: {} not found in Mach number list".format(mach_number))
def init_turn(starting, mach_number):
    max_turn = max_turn_angle(mach_number)
    print(max_turn)
    for i in range(4):
        turning_angles_init.append(starting + (((max_turn-starting)/3) * i))

def mach_list(range_start, range_final, gamma, mach_start):
    for i in range(range_start, range_final):
        internal_mach = mach_start + i/100
        list_M.append(internal_mach)
        mach_angle(internal_mach, list = True)
        prandtl_meyer(internal_mach, gamma)
        area_ratio(internal_mach, 1.4)
        area_ratio(internal_mach, 1.2)
        list_counter.append(i)
    array_new = np.stack((list_counter, list_M, list_angle_M, list_PMV_deg, list_final_ratio, list_final_ratio_1_4), axis = -1)

    return array_new

def mach_angle(mach_number, list = True):
    angle_M = m.asin(1/mach_number)
    angle_M_deg = ((angle_M/m.pi) * 180)
    if list == True:
        list_angle_M.append(round(angle_M_deg, 2))
    else:
        list_angle_M_MoC.append(round(angle_M_deg, 2))


def prandtl_meyer(mach_number, gamma):
    part_A = m.sqrt((gamma+1)/(gamma-1))
    part_B = (mach_number ** 2) - 1
    part_C = (gamma - 1)/(gamma + 1)
    part_D = m.sqrt(part_C * part_B)
    part_E = m.atan(part_D)
    part_F = m.atan(m.sqrt(part_B))

    final_combine = (part_A * part_E) - part_F
    list_PMV.append(final_combine)
    final_combine_deg = (final_combine/m.pi) * 180
    list_PMV_deg.append(round(final_combine_deg,2))



def area_ratio(mach_number, gamma):
    part_A = 1/mach_number
    part_B = 2/(gamma+1)
    part_C = (1 + ((gamma-1)/2) * mach_number ** 2)
    part_D = ((gamma+1)/(2 * (gamma-1)))
    final_ratio = part_A * ((part_B * part_C) ** part_D)
    if gamma == 1.2:
        list_final_ratio.append(final_ratio)
    elif gamma == 1.4:
        list_final_ratio_1_4.append(final_ratio)
    else:
        print("Gamma value is not 1.2 or 1.4, please modify function area_ratio to fix!")


def output_to_excel(array_1, array_2):
    df1 = pd.DataFrame(array_1, columns = ['counter','M', 'angle_M', 'PMV_deg', 'A/A*', 'A/A* for 1.4'])
    df2 = pd.DataFrame(array_2, columns = ['Points','R+','R-','theta','v','M','u','theta+u','theta-u','x','y'])
    writer = pd.ExcelWriter('C:/Users/Hubert/github/4fun/aero-thermo/mach_list.xlsx', engine = 'xlsxwriter')
    df1.to_excel(writer, 'Sheet2')
    df2.to_excel(writer, 'Sheet1')
    writer.save()



def find_nearest(i):
    pos = bisect_left(list_PMV_deg, PMV_deg_MoC[i])
    if pos > 300:
        pos = 300
    if pos == 0:
        new_M = list_M[0]
    if pos == len(list_PMV_deg):
        new_M = list_M[-1]
    before = list_PMV_deg[pos -1]
    try:
        after = list_PMV_deg[pos]
    except IndexError as error:
        print("current pos not found : {}".format(pos))
    if after - PMV_deg_MoC[i] < PMV_deg_MoC[i] - before:
        new_M = list_M[pos]
    else:
        new_M = list_M[pos-1]
    return new_M

def linear_interpolation(i):
    #new_M = np.interp(PMV_deg_MoC[i], list_PMV_deg, list_M)
    new_M = find_nearest(i)
    list_M_MoC.append(new_M)
    mach_angle(new_M, list = False)
    theta_minus_u = final_turning_angles[i] - list_angle_M_MoC[i]
    turn_minus_mach_angle.append(theta_minus_u)
    theta_plus_u = final_turning_angles[i] + list_angle_M_MoC[i]
    turn_plus_mach_angle.append(theta_plus_u)
def surface_point_geometry(i):
    if i == 4:
        k = i-4
    elif i == 9:
        k = i-4
    elif i == 13:
        k = i-3
    else:
        k = i-2
    alpha_point = 0.5*((turn_minus_mach_angle[k] + turn_minus_mach_angle[i]))
    alpha_point_rad = (alpha_point/180) * m.pi
    x_point_var = x_points[k] - (y_points[k]/m.tan(alpha_point_rad))
    x_points.append(x_point_var)
    y_points.append(0)

def wall_point_geometry(i,j):
    #i is current point number
    #j is previous wall point number
    alpha_point_a = turn_plus_mach_angle[i-1]
    alpha_point_rad_a = (alpha_point_a/180) * m.pi
    alpha_point_b = 0.5 * ((final_turning_angles[j]+final_turning_angles[i]))
    alpha_point_rad_b = (alpha_point_b/180) * m.pi
    x_point_var_numerator = (x_points[j] * m.tan(alpha_point_rad_b)) - (x_points[i-1] * m.tan(alpha_point_rad_a)) + y_points[i-1] - y_points[j]
    x_point_var_denominator = m.tan(alpha_point_rad_b) - m.tan(alpha_point_rad_a)
    x_point_var = x_point_var_numerator/x_point_var_denominator
    y_point_var = y_points[i-1] + ((x_point_var - x_points[i-1]) * m.tan(alpha_point_rad_a))
    x_points.append(x_point_var)
    y_points.append(y_point_var)

def floating_point_geometry(i):
    #i is current point number
    #j is previous point number positive above coordinate wise
    #k is previous point number negative below coordinate wise
    k = i-1
    j = i-4
    alpha_point_a = 0.5*((turn_plus_mach_angle[k] + turn_plus_mach_angle[i]))
    alpha_point_rad_a = (alpha_point_a/180) * m.pi
    alpha_point_b = 0.5*((turn_minus_mach_angle[j] + turn_minus_mach_angle[i]))
    alpha_point_rad_b = (alpha_point_b/180) * m.pi
    x_point_var_numerator = (x_points[i-4] * m.tan(alpha_point_rad_b)) - (x_points[k] * m.tan(alpha_point_rad_a)) + y_points[k] - y_points[j]
    x_point_var_denominator = m.tan(alpha_point_rad_b) - m.tan(alpha_point_rad_a)
    x_point_var = x_point_var_numerator/x_point_var_denominator
    y_point_var = y_points[k] + ((x_point_var - x_points[k]) * m.tan(alpha_point_rad_a))
    x_points.append(x_point_var)
    y_points.append(y_point_var)

def geometry(i):
    if (0 <= i <= 3):
        x_points.append(0)
        y_points.append(1)
    elif i == 4:
        surface_point_geometry(i)
    elif (5 <= i <= 7):
        floating_point_geometry(i)
    elif i == 8:
        wall_point_geometry(i,3)
    elif i == 9:
        surface_point_geometry(i)
    elif (10 <= i < 12):
        floating_point_geometry(i)
    elif i == 12:
        wall_point_geometry(i, 8)
    elif i == 13:
        surface_point_geometry(i)
    elif (14 <= i < 15):
        floating_point_geometry(i)
    elif i == 15:
        wall_point_geometry(i, 12)
    elif i == 16:
        surface_point_geometry(i)
    elif i == 17:
        wall_point_geometry(i, 15)
    else:
        print("Invalid point number!")

def MoC_Table(turning_angles_init, no_of_points):
    for i in range(4):
        final_turning_angles.append(turning_angles_init[i])
        PMV_deg_MoC.append(turning_angles_init[i])
        list_R_positive.append(0)
        list_R_minus.append(turning_angles_init[i] * 2)
        linear_interpolation(i)
        geometry(i)

    for i in range(4,8):
        list_R_minus.append(list_R_minus[i-4])
        list_R_positive.append(list_R_minus[0])
        final_turning_angles.append((list_R_minus[i] - list_R_positive[i])/2)
        PMV_deg_MoC.append(list_R_positive[i] + final_turning_angles[i])
        linear_interpolation(i)
        geometry(i)

    #wall point 5

    for i in range(8,9):
        list_R_minus.append('-')
        list_R_positive.append(list_R_positive[i-1])
        final_turning_angles.append(final_turning_angles[i-1])
        PMV_deg_MoC.append(PMV_deg_MoC[i-1])
        linear_interpolation(i)
        geometry(i)


    for i in range(9,12):
        list_R_minus.append(list_R_minus[i-8])
        list_R_positive.append(list_R_minus[1])
        final_turning_angles.append((list_R_minus[i] - list_R_positive[i])/2)
        PMV_deg_MoC.append(list_R_positive[i] + final_turning_angles[i])
        linear_interpolation(i)
        geometry(i)

    #wall point 9

    for i in range(12,13):
        list_R_minus.append('-')
        list_R_positive.append(list_R_positive[i-1])
        final_turning_angles.append(final_turning_angles[i-1])
        PMV_deg_MoC.append(PMV_deg_MoC[i-1])
        linear_interpolation(i)
        geometry(i)
    for i in range(13,15):
        list_R_minus.append(list_R_minus[i-11])
        list_R_positive.append(list_R_minus[2])
        final_turning_angles.append((list_R_minus[i] - list_R_positive[i])/2)
        PMV_deg_MoC.append(list_R_positive[i] + final_turning_angles[i])
        linear_interpolation(i)
        geometry(i)

    #wall point 12
    for i in range(15,16):
        list_R_minus.append('-')
        list_R_positive.append(list_R_positive[i-1])
        final_turning_angles.append(final_turning_angles[i-1])
        PMV_deg_MoC.append(PMV_deg_MoC[i-1])
        linear_interpolation(i)
        geometry(i)
    for i in range(16,17):
        list_R_minus.append(list_R_minus[i-13])
        list_R_positive.append(list_R_minus[3])
        final_turning_angles.append((list_R_minus[i] - list_R_positive[i])/2)
        PMV_deg_MoC.append(list_R_positive[i] + final_turning_angles[i])
        linear_interpolation(i)
        geometry(i)
    for i in range(17,18):
        list_R_minus.append('-')
        list_R_positive.append(list_R_positive[i-1])
        final_turning_angles.append(final_turning_angles[i-1])
        PMV_deg_MoC.append(PMV_deg_MoC[i-1])
        linear_interpolation(i)
        geometry(i)
    #print(final_turning_angles)
    #print(PMV_deg_MoC)
    #print(list_R_positive)
    #print(list_R_minus)
    #print(list_M_MoC)
    #print(list_angle_M_MoC)
    #print(turn_minus_mach_angle)
    #print(turn_plus_mach_angle)
    array_MoC= np.stack((point_list,list_R_positive,list_R_minus,final_turning_angles,PMV_deg_MoC,list_M_MoC,list_angle_M_MoC,turn_plus_mach_angle,turn_minus_mach_angle, x_points,y_points), axis = -1)

    return array_MoC

def plot_nozzle():
    x_points_1 = []
    y_points_1 = []
    x_points_2 = []
    y_points_2 = []
    x_points_3 = []
    y_points_3 = []
    x_points_4 = []
    y_points_4 = []
    x_points_upper = []
    y_points_upper = []
    legend = []
    for i in range(0,4):
        while i == 0:
            x_points_1.append(x_points[i])
            y_points_1.append(y_points[i])
            legend.append(i)
            x_points_upper.append(x_points[i])
            y_points_upper.append(y_points[i])
            for i in range(4,9):
                x_points_1.append(x_points[i])
                y_points_1.append(y_points[i])
                if i == 8:
                    x_points_upper.append(x_points[i])
                    y_points_upper.append(y_points[i])
            plt.plot(x_points_1,y_points_1)
        while i == 1:
            x_points_2.append(x_points[i])
            y_points_2.append(y_points[i])
            legend.append(i)
            for i in range(9,13):
                x_points_2.append(x_points[i])
                y_points_2.append(y_points[i])
                if i == 12:
                    x_points_upper.append(x_points[i])
                    y_points_upper.append(y_points[i])
            plt.plot(x_points_2, y_points_2)
        while i == 2:
            x_points_3.append(x_points[i])
            y_points_3.append(y_points[i])
            legend.append(i)
            for i in range(13,16):
                x_points_3.append(x_points[i])
                y_points_3.append(y_points[i])
                if i == 15:
                    x_points_upper.append(x_points[i])
                    y_points_upper.append(y_points[i])
            plt.plot(x_points_3, y_points_3)
        while i == 3:
            x_points_4.append(x_points[i])
            y_points_4.append(y_points[i])
            legend.append(i)
            for i in range(16,18):
                x_points_4.append(x_points[i])
                y_points_4.append(y_points[i])
                if i == 17:
                    x_points_upper.append(x_points[i])
                    y_points_upper.append(y_points[i])
            plt.plot(x_points_4, y_points_4)
    curve = interpolate.interp1d(x_points_upper, y_points_upper, kind = 'cubic')
    new_x = np.linspace(0,x_points_upper[-1],100)
    plt.plot(new_x, curve(new_x), '--')
    plt.axvline(x= x_points_upper[-1])
    plt.text(x_points_upper[-1] + 0.5, y_points_upper[-1], 'x ={}, y = {}'.format(round(x_points_upper[-1],2), round(y_points_upper[-1],2)))
    plt.axis([0,35,0,10])
    plt.legend(legend, loc ="upper left")
    plt.show()

array_1 = mach_list(0,301, 1.4, 1)
init_turn(1.00,3.2)
array_2 = MoC_Table(turning_angles_init, 14)
output_to_excel(array_1,array_2)
plot_nozzle()

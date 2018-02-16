import numpy as np
import os

print "ok"

if os.path.isfile("tower_sections.csv"):
    print "reading section inputs"
else:
    print "tower_sections.csv not found"

#section_no-0, can_no_base-1, can_no_top-2, height_flange_base-3, height_flange_top-4
tower_sections = np.genfromtxt('tower_sections.csv', delimiter=',', skip_header=1)
total_sections = int(np.shape(tower_sections)[0])
print "number of sections read - " + str(total_sections)

if os.path.isfile("tower_cans.csv"):
    print "reading can inputs"

#can_no-0, can_height_bottom-1, can_height_top-2, can_outer_dia_bottom-3, can_outer_dia_top-4, 
#can_inner_dia_bottom-5, can_inner_dia_top-6, section_modulus_bottom-7, section_modulus_top-8
tower_cans = np.genfromtxt('tower_cans.csv', delimiter=',', skip_header=1)

total_cans = int(np.shape(tower_cans)[0])
print "number of cans read - " + str(total_cans)

assert tower_sections[total_sections-1][2] == total_cans , "mismatch in can number"

# total weld points = total number of cans + total number of sections
total_fatigue_points = total_cans + total_sections
tower_fatigue_points = np.zeros( shape = (total_fatigue_points, 6) )

#can_no-0, can_height_bottom-1, can_height_top-2, can_outer_dia_bottom-3, can_outer_dia_top-4, 
#can_inner_dia_bottom-5, can_inner_dia_top-6, section_modulus_bottom-7, section_modulus_top-8
fatigue_point_counter = 0

for row in tower_sections:
    for i in range(   int(row[1])-1, int(row[2])  ):
        print i
        temp = np.zeros(6)
        temp[0] = tower_cans[i][1]  # Column C
        temp[1] = tower_cans[i][3]  # Column D
        temp[2] = (tower_cans[i][3] - tower_cans[i][5]) / 2 # Column E
        temp[3] = (tower_cans[i][4] - tower_cans[i][6]) / 2 # Column F
        
        # Column G and H
        if i == int(row[1])-1: # first weld point of a section
            temp[4] = temp[5] = tower_cans[i][7]
        else:
            temp[4] = tower_cans[i-1][7]
            temp[5] = tower_cans[i][7]
        
        tower_fatigue_points[fatigue_point_counter] = temp
        fatigue_point_counter+=1
        print temp

        # for last can of each section 2 weld points are calculated
        if i == int(row[2]) -1:
            temp = np.zeros(6)
            temp[0] = tower_cans[i][2]  # Column C
            temp[1] = tower_cans[i][3]  # Column D
            temp[2] = temp[3] = (tower_cans[i][4] - tower_cans[i][6]) / 2 # Column E and F
            # Column G and H # above and below section modulus will be same for top weld point in each section
            temp[4] = temp[5] = tower_cans[i][8]
            tower_fatigue_points[fatigue_point_counter] = temp
            fatigue_point_counter+=1
            print temp       
    print "-"    

np.savetxt('tower_fatigue.csv', tower_fatigue_points, fmt='%0.3f', delimiter=',')
    


# np.apply_along_axis( myfunction, axis=1, arr=mymatrix ) # for applying a function to each row
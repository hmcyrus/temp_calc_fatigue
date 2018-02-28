import numpy as np
import os

def calc_tan_alpha(d_base, d_top, h):    
    # print "calc_tan_alpha"
    return ((d_base - d_top) / 2) / h

def calc_scf_total(cone1, cone2, inner, outer):
    cone = max (cone1, cone2)
    total_inner = (inner -1 ) + (cone - 1) + 1
    total_outer = (outer -1) + (cone -1) + 1
    return max(total_inner, total_outer)

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

if os.path.isfile("tower_options.csv"):
    print "reading tower_options"

# dc_weld-0, dc_bracket-1, calc_SCF_butt-2, calc_SCF_cone-3, calc_SCF_flange-4, weld_prep_angle-5, weld_ground_flush-6
# joint_type-7, max_misalignment_accidental_eccentricity-8, additional_SCF-9, quality_class-10, Ue_max-11,
# thickness_exponent_weld-12, t_ref-13, fatigue_material_factor-14, DEL_Nref-15, N-16, m1-17, m2-18, loga1-19, loga2-20 
# N_bracket-21, m1_bracket-22, m2_bracket-23, loga1_bracket-24, loga2_bracket-25, DEL_m-26
tower_options = np.genfromtxt('tower_options.csv', delimiter=',', skip_header=1, dtype='unicode')

# total weld points = total number of cans + total number of sections
total_fatigue_points = total_cans + total_sections
tower_fatigue_points = np.zeros( shape = (total_fatigue_points, 27) )

if os.path.isfile("tower_cans_del_my.csv"):
    print "reading del_my"

tower_del_my = np.genfromtxt('tower_cans_del_my.csv', delimiter=',', skip_header=1)
assert int(np.shape(tower_del_my)[0]) == total_fatigue_points, "correct number of del_my"

#can_no-0, can_height_bottom-1, can_height_top-2, can_outer_dia_bottom-3, can_outer_dia_top-4, 
#can_inner_dia_bottom-5, can_inner_dia_top-6, section_modulus_bottom-7, section_modulus_top-8
fatigue_point_counter = 0

for row in tower_sections:
    for i in range(   int(row[1])-1, int(row[2])  ):
        # print i
        temp = np.zeros(27)
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
        
        # Column S
        temp[6] = min( float(tower_options[8]), float( tower_options[11] )* ((temp[2] + temp[3])/2) )
        
        # Column V
        temp[7] = 0.5 * (max( temp[2], temp[3]) - min( temp[2], temp[3]))

        # Column W,X
        temp[8] = temp[9] = 0.1 * min( temp[2], temp[3])

        # Column Y
        temp[10] = 1 - ( 3. * ((-1)* float(tower_options[8]) + temp[7] + temp[9]) ) / ( min( temp[2], temp[3]) * ( 1 + ( ( max( temp[2], temp[3]) * 0.5 ) / ( min( temp[2], temp[3]) * 0.5 ) ) ) ) 
        
        # Column Z 
        temp[11] = 1 + ( 3. * ( float(tower_options[8]) + temp[7] + (-1)*temp[8]) ) / ( min( temp[2], temp[3]) * ( 1 + ( ( max( temp[2], temp[3]) * 0.5 ) / ( min( temp[2], temp[3]) * 0.5 ) ) ) ) 

        # Column AB
        temp[12] = 1. + ( 0.6 * max( temp[2], temp[3]) * np.sqrt( (temp[2] + temp[3]) * temp[1] ) * calc_tan_alpha( tower_cans[i][3], tower_cans[i][4], temp[0]) ) / max( temp[2], temp[3]) ** 2
        
        # Column AC
        temp[13] = 1. + ( 0.6 * max( temp[2], temp[3]) * np.sqrt( (temp[2] + temp[3]) * temp[1] ) * calc_tan_alpha( tower_cans[i][5], tower_cans[i][6], temp[0]) ) / min( temp[2], temp[3]) ** 2

        # def calc_scf_total(cone1, cone2, inner, outer):
        # Column AD
        temp[14] = calc_scf_total(temp[12], temp[13], temp[11], temp[10])
        
        # Column AJ # the division by 10^3 is for unit adjustment
        temp[15] = (tower_del_my[fatigue_point_counter] / min(temp[4], temp[5]) ) / 1000

        # Column AK #dc_weld
        temp[16] = tower_options[0]

        # Column AL
        temp[17] = tower_options[12]
        
        # Column AM 
        temp[18] = ( max(temp[2], temp[3]) / float(tower_options[13]) ) ** temp[17]

        # Column AN
        sigma_ref_en = 10 ** ( ( float(tower_options[19]) - np.log10(  float(tower_options[16]) )  ) / float(tower_options[17]) )
        temp[19] = sigma_ref_en / (temp[18] * float(tower_options[14]) * temp[14])

        # Column AO
		# DEL_m comes from D39 of General_Inputs sheet
        temp[20] = 10**( np.log10(2e6) + float(tower_options[26]) * (np.log10(temp[19]) - np.log10(temp[15])) )

        # Column AP
        temp[21] = float(tower_options[15])/temp[20]

        # Column AQ
        temp[22] = ( ( 1 / temp[21]**(1/ float(tower_options[17]) ) ) - 1 ) * 100

        # Column AR
        temp[23] = float(tower_options[1])

        # Column AS
        # sigma_ref_bracket = 10 ** ( ( float( tower_options[24]) - np.log10( float( tower_options[21]) ) ) / float(tower_options[22]) )
		# numerical value 3 is used in place of m1
        sigma_ref_bracket = 10**( ( float( tower_options[24]) - np.log10(2e6) ) / 3 )
        sigma_ref_bracket_factored = sigma_ref_bracket / ( float( tower_options[9]) * float(tower_options[14]) )        
        temp[24] = 10**( np.log10( float( tower_options[21]) ) + float(tower_options[26]) * (np.log10(sigma_ref_bracket_factored) - np.log10(temp[15]) )

        # Column AT
        print tower_options[15]
        print temp[24]
        temp[25] = float(tower_options[15]) + float(temp[24])

        # Column AU
        temp[26] = ( ( 1 / temp[25]**(1/ float( tower_options[22]))) - 1 ) * 100

        tower_fatigue_points[fatigue_point_counter] = temp
        fatigue_point_counter+=1
        # print temp

        # for last can of each section 2 weld points are calculated
        if i == int(row[2]) -1:
            temp = np.zeros(27)
            temp[0] = tower_cans[i][2]  # Column C
            temp[1] = tower_cans[i][3]  # Column D
            temp[2] = temp[3] = (tower_cans[i][4] - tower_cans[i][6]) / 2 # Column E and F
            # Column G and H # above and below section modulus will be same for top weld point in each section
            temp[4] = temp[5] = tower_cans[i][8]
            # Column S
            temp[6] = min( float(tower_options[8]), float( tower_options[11] )* ((temp[2] + temp[3])/2) )
            #Column V
            temp[7] = 0.5 * (max( temp[2], temp[3]) - min( temp[2], temp[3]))
            # Column W,X
            temp[8] = temp[9] = 0.1 * min( temp[2], temp[3])    
            # Column Y
            temp[10] = 1 - ( 3. * ((-1)* float(tower_options[8]) + temp[7] + temp[9]) ) / ( min( temp[2], temp[3]) * ( 1 + ( ( max( temp[2], temp[3]) * 0.5 ) / ( min( temp[2], temp[3]) * 0.5 ) ) ) ) 
            # Column Z 
            temp[11] = 1 + ( 3. * ( float(tower_options[8]) + temp[7] + (-1)*temp[8]) ) / ( min( temp[2], temp[3]) * ( 1 + ( ( max( temp[2], temp[3]) * 0.5 ) / ( min( temp[2], temp[3]) * 0.5 ) ) ) ) 
            # Column AB
            temp[12] = 1. + ( 0.6 * max( temp[2], temp[3]) * np.sqrt( (temp[2] + temp[3]) * temp[1] ) * calc_tan_alpha( tower_cans[i][3], tower_cans[i][4], temp[0]) ) / max( temp[2], temp[3]) ** 2
            # Column AC
            temp[13] = 1. + ( 0.6 * max( temp[2], temp[3]) * np.sqrt( (temp[2] + temp[3]) * temp[1] ) * calc_tan_alpha( tower_cans[i][5], tower_cans[i][6], temp[0]) ) / min( temp[2], temp[3]) ** 2
            # def calc_scf_total(cone1, cone2, inner, outer):
            # Column AD
            temp[14] = calc_scf_total(temp[12], temp[13], temp[11], temp[10])
            # Column AJ # the division by 10^3 is for unit adjustment
            temp[15] = (tower_del_my[fatigue_point_counter] / min(temp[4], temp[5]) ) / 1000
            # Column AK #dc_weld
            temp[16] = tower_options[0]
            # Column AL
            temp[17] = tower_options[12]            
            # Column AM 
            temp[18] = ( max(temp[2], temp[3]) / float(tower_options[13]) ) ** temp[17]
            # Column AN
            sigma_ref_en = 10 ** ( ( float(tower_options[19]) - np.log10(  float(tower_options[16]) )  ) / float(tower_options[17]) )
            temp[19] = sigma_ref_en / (temp[18] * float(tower_options[14]) * temp[14])
            # Column AO
            # DEL_m comes from D39 of General_Inputs sheet
            temp[20] = 10**( np.log10(2e6) + float(tower_options[26]) * (np.log10(temp[19]) - np.log10(temp[15])) )
            # Column AP
            temp[21] = float(tower_options[15])/temp[20]
            # Column AQ
            temp[22] = ( ( 1 / temp[21]**(1/ float(tower_options[17]) ) ) - 1 ) * 100
            # Column AR
            temp[23] = float(tower_options[1])
            # Column AS
            # sigma_ref_bracket = 10 ** ( ( float( tower_options[24]) - np.log10( float( tower_options[21]) ) ) / float(tower_options[22]) )
            # numerical value 3 is used in place of m1
            sigma_ref_bracket = 10**( ( float( tower_options[24]) - np.log10(2e6) ) / 3 )
            sigma_ref_bracket_factored = sigma_ref_bracket / ( float( tower_options[9]) * float(tower_options[14]) )        
            temp[24] = 10**( np.log10( float( tower_options[21]) ) + float(tower_options[26]) * (np.log10(sigma_ref_bracket_factored) - np.log10(temp[15]) )
            # Column AT
            temp[25] = float(tower_options[15]) / temp[24]
            # Column AU
            temp[26] = ( ( 1 / temp[25]**(1/ float( tower_options[22]))) - 1 ) * 100            
            
            tower_fatigue_points[fatigue_point_counter] = temp
            fatigue_point_counter+=1
            # print temp       
    print "-"    

np.savetxt('tower_fatigue.csv', tower_fatigue_points, fmt='%0.4f', delimiter=',')
    


# np.apply_along_axis( myfunction, axis=1, arr=mymatrix ) # for applying a function to each row


import numpy as np
import os

def calc_tan_alpha(d_base, d_top, h):    
    return ((d_base - d_top) / 2) / h

def calc_diff_in_alpha(d_base_prev, d_top_prev, h_prev, d_base_current, d_top_current, h_current):
    tan_alpha_prev = ((d_base_prev - d_top_prev) / 2) / h_prev
    tan_alpha_current = ((d_base_current - d_top_current) / 2) / h_current
    print np.arctan(tan_alpha_current) - np.arctan(tan_alpha_prev)
    return np.arctan(tan_alpha_current) - np.arctan(tan_alpha_prev)

def scf_total_can(scf_cone_outer, scf_cone_inner, scf_butt_weld_outer, scf_butt_weld_inner ):
    cone = max (scf_cone_outer, scf_cone_inner)
    total_inner = (scf_butt_weld_inner -1 ) + (cone - 1) + 1
    total_outer = (scf_butt_weld_outer -1) + (cone -1) + 1
    return max(total_inner, total_outer, 1.)

###### calculates max_misalignment_en1991 of a single can
def max_misalignment_en1991_can(max_misalignment, ue_max, t_above, t_below): 
    max_misalignment_en1991 = min( max_misalignment, ue_max*((t_above + t_below)/2) )
    return max_misalignment_en1991

###### calculates ecc_thickness of a single can
def ecc_thickness_can():
    ecc_thickness = 0.0 # * (max_t - min_t)
    return ecc_thickness

###### calculates misalign_SN_inner and misalign_SN_outer of a single can and returns them in an array in same order
def misalign_SN_inner_and_misalign_SN_outer_can(max_t, min_t):
    if max_t == min_t:
        misalign_SN_inner = misalign_SN_outer = 0.1 * min_t        
    else:
        misalign_SN_inner = misalign_SN_outer = 0.1 * min_t    
    return np.array([misalign_SN_inner, misalign_SN_outer])

###### calculates scf_butt_weld_outer and scf_butt_weld_inner of a single can and returns them in an array in same order
def scf_butt_weld_outer_and_scf_butt_weld_inner_can(max_misalignment_en1991, ecc_thickness, misalign_SN_outer, misalign_SN_inner, max_t, min_t):
    if max_t == min_t:
        scf_butt_weld_outer = max(1 + 3*(max_misalignment_en1991 - misalign_SN_outer)/max_t, 1.0)
    else:
        scf_butt_weld_outer = 1 + ( 6. * ( max_misalignment_en1991 + ecc_thickness - misalign_SN_outer) ) / ( min_t * ( 1 + ( ( max_t ** 1.5 ) / ( min_t ** 1.5 )))) 
    
    if max_t == min_t:
        scf_butt_weld_inner = scf_butt_weld_outer
    else:
        scf_butt_weld_inner = 1 + ( 6. * ( max_misalignment_en1991 + ecc_thickness + (-1)*misalign_SN_inner) ) / ( min_t * ( 1 + ( ( max_t ** 1.5 ) / ( min_t ** 1.5 ) ) ) ) 
    
    return np.array([scf_butt_weld_outer, scf_butt_weld_inner]) 

###### calculates scf_cone_outer and scf_cone_inner of a single can and returns them in an array in same order
def scf_cone_outer_and_scf_cone_inner_can(t_below, t_above, dia, can_outer_dia_bottom_prev, can_outer_dia_top_prev, can_height_prev, can_outer_dia_bottom, can_outer_dia_top, can_height):        
    if(np.abs( calc_diff_in_alpha( can_outer_dia_bottom_prev, can_outer_dia_top_prev, can_height_prev, can_outer_dia_bottom, can_outer_dia_top, can_height)) < 1e-03 ):
        scf_cone_outer = 1.
    else:
        scf_cone_outer = 1. + ( 0.6 * t_below * np.sqrt( (t_below + t_above) * dia ) * calc_tan_alpha(can_outer_dia_bottom, can_outer_dia_top, can_height) ) / t_below ** 2
    
    if(np.abs( calc_diff_in_alpha( can_outer_dia_bottom_prev, can_outer_dia_top_prev, can_height_prev, can_outer_dia_bottom, can_outer_dia_top, can_height)) < 1e-03 ):
        scf_cone_inner = 1.
    else:        
        scf_cone_inner = 1. + ( 0.6 * t_below * np.sqrt( (t_above + t_below) * dia ) * calc_tan_alpha(can_outer_dia_bottom, can_outer_dia_top, can_height) ) / t_above ** 2
    
    return np.array([scf_cone_outer, scf_cone_inner])

###### calculates des of a single can
###### the division by 10^3 is for unit adjustment
def des_can(del_m_y, w_above, w_below):    
    des = (del_m_y / min(w_above, w_below) ) / 1000
    return des

###### calculates thickness_factor of a single can
def thickness_factor_can(max_t, t_ref, thickness_exponent_weld):    
    if max_t > float(t_ref):
        thickness_factor = ( max_t / float(t_ref) ) ** float(thickness_exponent_weld)
    else:
        thickness_factor = 1.
    return thickness_factor

###### calculates sigma_ref_EN_weld_factored of a single can
def sigma_ref_en_weld_factored_can(loga1_weld, n_weld, m1_weld, thickness_factor, fatigue_material_factor, total_SCF):    
    sigma_ref_weld = 10 ** ( (loga1_weld - np.log10(n_weld) ) / m1_weld)
    sigma_ref_weld_factored = sigma_ref_weld / (thickness_factor * fatigue_material_factor * total_SCF)
    return sigma_ref_weld_factored

###### calculates n_allowable_weld, damage_weld, DEL_margin_fatigue_weld of a single can and returns them in an array in same order
def margin_fatigue_weld_can(sigma_ref_en_weld_factored, del_m, des, del_nref):
    n_allowable_weld = 10**( np.log10(2e6) + del_m * (np.log10(sigma_ref_en_weld_factored) - np.log10(des)) )
    damage_weld = del_nref/n_allowable_weld    
    del_margin_fatigue_weld = ( ( 1 / damage_weld**(1/ del_m ) ) - 1 ) * 100  
    return np.array([n_allowable_weld, damage_weld, del_margin_fatigue_weld])

###### calculates sigma_ref_bracket of a single can
def sigma_ref_bracket_factored_can(loga1_bracket, scf_additional, fatigue_material_factor):
    sigma_ref_bracket = 10**( ( loga1_bracket - np.log10(2e6) ) / 3. ) 
    sigma_ref_bracket_factored = sigma_ref_bracket / ( scf_additional * fatigue_material_factor )        
    return sigma_ref_bracket_factored

###### calculates N_allow_brackets, damage_brackets, DEL_margin_fatigue_brackets of a single can and returns them in an array in same order
def margin_fatigue_brackets_can(n_bracket, sigma_ref_bracket_factored, del_m, des, del_nref):
    n_allowable_bracket = 10**( np.log10( n_bracket ) + del_m * ( np.log10(sigma_ref_bracket_factored) - np.log10(des) ) )       
    damage_bracket = del_nref/n_allowable_bracket    
    del_margin_fatigue_brackets = ( ( 1 / damage_bracket**(1/ del_m )) - 1 ) * 100
    return np.array([n_allowable_bracket, damage_bracket, del_margin_fatigue_brackets])

	# add column headers in output file
def single_can_calculation(max_misalignment, ue_max, t_below, t_above, dia, can_outer_dia_bottom, can_outer_dia_top, height, del_m_y_can, scf_additional,
                                w_above, w_below, dc_weld, dc_bracket, thickness_exponent_weld, t_ref, fatigue_material_factor, loga1_weld, n_weld, m1_weld,
                                del_m, del_nref, loga1_bracket, n_bracket, m1_bracket, can_height, can_outer_dia_bottom_prev, can_outer_dia_top_prev, can_height_prev):
    max_t = max(t_above, t_below)
    min_t = min(t_above, t_below)
    can_values = np.array([])
    
    # Column S # Maximum misalignment from EN1991-1-6
    max_misalignment_en1991 = max_misalignment_en1991_can(max_misalignment, ue_max, t_above, t_below)
    can_values = np.append(can_values, [max_misalignment_en1991])   

    # Column U #del_m_y
    can_values = np.append(can_values, [del_m_y_can])

    # Column V # ecc_thickness
    # for T==t ecc_thickness = 0
    ecc_thickness = ecc_thickness_can()
    can_values = np.append(can_values, [ecc_thickness])

    # # Column W,X # misalign_SN_inner, misalign_SN_outer
    # [0]- misalign_SN_inner  [1] - misalign_SN_outer,
    misalign_SN_array = misalign_SN_inner_and_misalign_SN_outer_can(max_t, min_t) 
    can_values = np.append( can_values, misalign_SN_array)    
    
    # # Column Y,Z # SCF_butt_weld_outer, SCF_butt_weld_inner 
    # [0] - outer, [1] - inner 
    scf_butt_weld_array = scf_butt_weld_outer_and_scf_butt_weld_inner_can(max_misalignment_en1991, ecc_thickness, misalign_SN_array[1], misalign_SN_array[0], max_t, min_t)
    can_values = np.append(can_values, scf_butt_weld_array)    

    # # Column AB,AC # SCF_cone_outer, SCF_cone_inner
    # [0] - outer, [1]- inner
    scf_cone_array = scf_cone_outer_and_scf_cone_inner_can(t_below, t_above, dia, can_outer_dia_bottom_prev, can_outer_dia_top_prev, can_height_prev, can_outer_dia_bottom, can_outer_dia_top, can_height)    
    can_values = np.append(can_values, scf_cone_array)
    
    # # Column AD # total_SCF
    total_SCF = scf_total_can(scf_cone_array[0], scf_cone_array[1], scf_butt_weld_array[0], scf_butt_weld_array[1])
    can_values = np.append(can_values, [total_SCF])
    
    # # Column AJ # DES 
    des = des_can(del_m_y_can, w_above, w_below)
    can_values = np.append(can_values, [des])
    
    # # Column AM # thickness_factor        
    thickness_factor = thickness_factor_can(max_t, t_ref, thickness_exponent_weld)
    can_values = np.append(can_values, [thickness_factor])

    # # Column AN # sigma_ref_EN_weld_factored    
    sigma_ref_weld_factored = sigma_ref_en_weld_factored_can(loga1_weld, n_weld, m1_weld, thickness_factor, fatigue_material_factor, total_SCF)
    can_values = np.append(can_values, [sigma_ref_weld_factored])

    # # Column AO, AP, AQ # N_allow_weld, damage_weld, DEL_margin_fatigue_weld
    # [0] - n_allowable_weld, [1] - damage_weld, [2] -del_margin_fatigue_weld
    margin_weld_array = margin_fatigue_weld_can(sigma_ref_weld_factored, del_m, des, del_nref)
    can_values = np.append(can_values, margin_weld_array)
    
    # # Column AS, AT, AU # N_allow_brackets, damage_brackets, DEL_margin_fatigue_brackets
    # [0] - N_allow_brackets, [1] - damage_brackets, [2] -DEL_margin_fatigue_brackets
    sigma_ref_bracket_factored = sigma_ref_bracket_factored_can(loga1_bracket, scf_additional, fatigue_material_factor)
    margin_brackets_array = margin_fatigue_brackets_can(n_bracket, sigma_ref_bracket_factored, del_m, des, del_nref)
    can_values = np.append(can_values, margin_brackets_array)
    
    return can_values


if os.path.isfile("tower_sections_input.csv"):
    print "reading section inputs"
else:
    print "tower_sections.csv not found"

#section_no-0, can_no_base-1, can_no_top-2, height_flange_base-3, height_flange_top-4
tower_sections = np.genfromtxt('tower_sections_input.csv', delimiter=',', skip_header=1)
total_sections = int(np.shape(tower_sections)[0])
print "number of sections read - " + str(total_sections)

if os.path.isfile("tower_cans_input.csv"):
    print "reading can inputs"

#can_no-0, can_height_bottom-1, can_height_top-2, can_outer_dia_bottom-3, can_outer_dia_top-4, 
#can_inner_dia_bottom-5, can_inner_dia_top-6, section_modulus_bottom-7, section_modulus_top-8
tower_cans = np.genfromtxt('tower_cans_input.csv', delimiter=',', skip_header=1)

total_cans = int(np.shape(tower_cans)[0])
print "number of cans read - " + str(total_cans)

assert tower_sections[total_sections-1][2] == total_cans , "mismatch in can number"

if os.path.isfile("tower_options_input.csv"):
    print "reading tower_options"

# dc_weld-0, dc_bracket-1, calc_SCF_butt-2, calc_SCF_cone-3, calc_SCF_flange-4, weld_prep_angle-5, weld_ground_flush-6
# joint_type-7, max_misalignment_accidental_eccentricity-8, additional_SCF-9, quality_class-10, Ue_max-11,
# thickness_exponent_weld-12, t_ref-13, fatigue_material_factor-14, DEL_Nref-15, N-16, m1-17, m2-18, loga1-19, loga2-20 
# N_bracket-21, m1_bracket-22, m2_bracket-23, loga1_bracket-24, loga2_bracket-25, DEL_m-26
tower_options = np.genfromtxt('tower_options_input.csv', delimiter=',', skip_header=1, dtype='unicode')

# total weld points = total number of cans + total number of sections
total_fatigue_points = total_cans + total_sections
tower_fatigue_points = np.zeros( shape = (total_fatigue_points, 27) )

if os.path.isfile("tower_cans_del_my_input.csv"):
    print "reading del_my"

tower_del_my = np.genfromtxt('tower_cans_del_my_input.csv', delimiter=',', skip_header=1)
assert int(np.shape(tower_del_my)[0]) == total_fatigue_points, "correct number of del_my"

#can_no-0, can_height_bottom-1, can_height_top-2, can_outer_dia_bottom-3, can_outer_dia_top-4, 
#can_inner_dia_bottom-5, can_inner_dia_top-6, section_modulus_bottom-7, section_modulus_top-8
fatigue_point_counter = 0

for row in tower_sections:
    for i in range(   int(row[1])-1, int(row[2])  ):
        if i == int(row[1])-1: # first weld point of a section
            print "bottom weld point of section-" + str(row[0])
            outer_dia_base_prev = outer_dia_top_prev = h_prev = 1
        else:
            outer_dia_base_prev = tower_cans[i-1][3]
            outer_dia_top_prev = tower_cans[i-1][4]
            h_prev = tower_cans[i-1][9]
        
        ### array used for storing all columns' value for a single can
        can_columns = np.zeros(27, dtype=float)
        h_can = tower_cans[i][1]  # Column C
        dia_can = tower_cans[i][3]  # Column D #max comparison for D is to be done here
        # t_bottom, t_top
        if i == 0 :
            t_below_can = t_above_can = (tower_cans[i][3] - tower_cans[i][5]) / 2 
        else:
            t_below_can =  (tower_cans[i-1][4] - tower_cans[i-1][6]) / 2 # t_below of a weld point comes from the Dtop, dtop of previous element
            t_above_can =  (tower_cans[i][3] - tower_cans[i][5]) / 2
        # Column G and H
        if i == 0: 
            section_modulus_below_can = section_modulus_above_can = (np.pi/(32*tower_cans[i][3]))*(tower_cans[i][3]**4 - tower_cans[i][5]**4)
        else:
            section_modulus_below_can = (np.pi/(32*tower_cans[i-1][4]))*(tower_cans[i-1][4]**4 - tower_cans[i-1][6]**4)
            section_modulus_above_can = (np.pi/(32*tower_cans[i][3]))*(tower_cans[i][3]**4 - tower_cans[i][5]**4)
        
        print fatigue_point_counter

        can_values = single_can_calculation(float(tower_options[8]), float(tower_options[11]), t_below_can, t_above_can, dia_can, tower_cans[i][3], tower_cans[i][4], 
        h_can, tower_del_my[fatigue_point_counter], float(tower_options[9]),        
        section_modulus_above_can, section_modulus_below_can, float(tower_options[0]), float(tower_options[1]), float(tower_options[12]), float(tower_options[13]), float(tower_options[14]),        
        float(tower_options[19]), float(tower_options[16]), float(tower_options[17]),        
        float(tower_options[26]), float(tower_options[15]), float(tower_options[24]), float(tower_options[21]), float(tower_options[22]), float(tower_cans[i][9]),
        outer_dia_base_prev, outer_dia_top_prev, h_prev )

        ### storing all columns' values in an array
        can_columns[0] = h_can
        can_columns[1] = dia_can
        can_columns[2] = t_below_can
        can_columns[3] = t_above_can
        can_columns[4] = section_modulus_below_can
        can_columns[5] = section_modulus_above_can
        can_columns[6:6+can_values.size] = can_values 
         
        tower_fatigue_points[fatigue_point_counter] = can_columns
        fatigue_point_counter+=1
        # print temp

        # for last can of each section 2 weld points are calculated
        if i == int(row[2]) -1:
            ### array used for storing all columns' value for a single can
            can_columns = np.zeros(27)
            h_can = tower_cans[i][2]  # Column C
            dia_can = tower_cans[i][3]  # Column D
            t_below_can = t_above_can = (tower_cans[i][4] - tower_cans[i][6]) / 2 # Column E and F
            # Column G and H # above and below section modulus will be same for top weld point in each section
            section_modulus_below_can = section_modulus_above_can = (np.pi/(32*tower_cans[i][4]))*(tower_cans[i][4]**4 - tower_cans[i][6]**4)       
            print "top weld point for section- " + str(int(row[0]))  # no need to add 1, section number starts from 1
            print fatigue_point_counter
            can_values = single_can_calculation(float(tower_options[8]), float(tower_options[11]), t_below_can, t_above_can, dia_can, tower_cans[i][3], tower_cans[i][4], 
                                        h_can, tower_del_my[fatigue_point_counter], float(tower_options[9]),        
                                        section_modulus_above_can, section_modulus_below_can, float(tower_options[0]), float(tower_options[1]), float(tower_options[12]), float(tower_options[13]), float(tower_options[14]),        
                                        float(tower_options[19]), float(tower_options[16]), float(tower_options[17]),        
                                        float(tower_options[26]), float(tower_options[15]), float(tower_options[24]), float(tower_options[21]), float(tower_options[22]), tower_cans[i][9],
                                        1., 1., 1.)
            
            ### storing all columns' values in an array
            can_columns[0] = h_can
            can_columns[1] = dia_can
            can_columns[2] = t_below_can
            can_columns[3] = t_above_can
            can_columns[4] = section_modulus_below_can
            can_columns[5] = section_modulus_above_can
            can_columns[6:6+can_values.size] = can_values 
            tower_fatigue_points[fatigue_point_counter] = can_columns
            fatigue_point_counter+=1
            # print temp       
    print "-end of a section"    

column_header = "H, D, t_below, t_above, w_below, w_above, max_misalignment_en1991, DEL_My, ecc_thickness, " + \
                " misalign_SN_inner, misalign_SN_outer, SCF_butt_weld_outer, SCF_butt_weld_inner, SCF_cone_outer, SCF_cone_inner, total_SCF," + \
                " DES, thickness_factor, sigma_ref_EN_weld_factored, N_allow_weld, damage_weld, DEL_margin_fatigue_weld," + \
                " N_allow_brackets, damage_brackets, DEL_margin_fatigue_brackets"
                
np.savetxt('tower_fatigue_output.csv', tower_fatigue_points, fmt='%0.10f', delimiter=',', header= column_header)    

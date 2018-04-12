# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:53:42 2018

@author: cyrus
"""
import numpy as np
import xlwings as xw
import os

def fetch_range_from_sheet(xw_sheet, cell_begin, cell_end):
    return xw_sheet.range(cell_begin + ':' + cell_end).value

#folder_path = "test_results\\j9\\plus"
#folder_path = "test_results\\j9\\minus"
#folder_path = "test_results\\k11\\plus"
#folder_path = "test_results\\k11\\minus"
#folder_path = "test_results\\k13\\plus"
folder_path = "test_results\\k13\\minus"
os.makedirs(folder_path)
##### read sections
towergeo_sheet = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm").sheets['Towergeo']

number_of_sections = 5

tower_sections = np.zeros( shape = (number_of_sections, 3) )  # 3 information of section is required for fatigue calculation
tower_sections[:, 0] = fetch_range_from_sheet(towergeo_sheet, "B9", "B13")  #section_no	 B9:B13
tower_sections[:, 1] = fetch_range_from_sheet(towergeo_sheet, "E9", "E13")  #can_no_base	E9:E13
tower_sections[:, 2] = fetch_range_from_sheet(towergeo_sheet, "F9", "F13")  #can_no_top  F9:F13
column_header = "section_no, can_no_base, can_no_top"
np.savetxt(folder_path + '\\tower_sections_script_input.csv', tower_sections, fmt='%0.10f', delimiter=',', header= column_header)

##### read cans
number_of_cans = 49

tower_cans = np.zeros( shape = (number_of_cans, 10) )  # 10 columns are here, but 8 information of section are used for fatigue calculation 
#(section_modulus_bottom and section_modulus_top are use after manually calculating)
tower_cans[:, 0] = range(1, number_of_cans+1)                                 # can_no
tower_cans[:, 1] = fetch_range_from_sheet(towergeo_sheet, "K25", "K73")       # can_height_bottom K
tower_cans[:, 2] = fetch_range_from_sheet(towergeo_sheet, "L25", "L73")       # can_height_top L 
tower_cans[:, 3] = fetch_range_from_sheet(towergeo_sheet, "M25", "M73")       # can_outer_dia_bottom M 
tower_cans[:, 4] = fetch_range_from_sheet(towergeo_sheet, "N25", "N73")       # can_outer_dia_top N
tower_cans[:, 5] = fetch_range_from_sheet(towergeo_sheet, "O25", "O73")       # can_inner_dia_bottom O
tower_cans[:, 6] = fetch_range_from_sheet(towergeo_sheet, "P25", "P73")       # can_inner_dia_top P
tower_cans[:, 7] = fetch_range_from_sheet(towergeo_sheet, "S25", "S73")       # section_modulus_bottom S
tower_cans[:, 8] = fetch_range_from_sheet(towergeo_sheet, "T25", "T73")       # section_modulus_top T
tower_cans[:, 9] = fetch_range_from_sheet(towergeo_sheet, "E25", "E73")       # height_can E

column_header = "can_no, can_height_bottom, can_height_top, can_outer_dia_bottom, can_outer_dia_top, can_inner_dia_bottom, " + \
                "can_inner_dia_top, section_modulus_bottom, section_modulus_top, height_can"
np.savetxt(folder_path + '\\tower_cans_script_input.csv', tower_cans, fmt='%0.10f', delimiter=',', header= column_header)

##### read DEL_My_interpolated
f_loads_sheet = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm").sheets['F_Loads']
tower_del_my = np.zeros( shape = (number_of_cans + number_of_sections, 1) ) # here we fetch only one column

tower_del_my[:, 0] = fetch_range_from_sheet(f_loads_sheet, "K10", "K63")

column_header = "del_my"
np.savetxt(folder_path + '\\tower_cans_del_my_script_input.csv', tower_del_my, fmt='%0.10f', delimiter=',', header= column_header)

##### read options
tower_options = np.empty( shape = (1, 27), dtype=object) #np.zeros(27) # upto column AA #tower_options = {}
 
tower_options[:, 0] = 90  # Fatigue(I)  #tower_options['dc_weld'] 
tower_options[:, 1] = 80  # Fatigue(J) #tower_options['dc_bracket'] 
tower_options[:, 2] = 'DNVGL_butt' # Fatigue(K) #tower_options['calc_SCF_butt']
tower_options[:, 3] = 'TRUE' # Fatigue(L) #tower_options['calc_SCF_cone']
tower_options[:, 4] = 'FALSE' # Fatigue(M) #tower_options['calc_SCF_flange']
tower_options[:, 5] = 30 # Fatigue(N) #tower_options['weld_prep_angle'] 
tower_options[:, 6] = 'FALSE' # Fatigue(O) #tower_options['weld_ground_flush']
tower_options[:, 7] = 'Standandrd' # Fatigue(P) #tower_options['joint_type']
tower_options[:, 8] = 0.0030 # Fatigue(Q) #tower_options['max_misalignment']
tower_options[:, 9] = 1 # Fatigue(R) #tower_options['scf_additional']
tower_options[:, 10] = 'B' # Fatigue(R6) #tower_options['quality_class']
tower_options[:, 11] = 0.2 # from the Accidental eccentricity tolerance table in fatigue sheet # Fatigue(S4) #tower_options['ue_max']
tower_options[:, 12] = 0.2 # Library(J) #tower_options['thickness_exponent_weld']
tower_options[:, 13] = 0.025 # source not found #tower_options['t_ref']
tower_options[:, 14] = 1.265 # General_Inputs(D25) #tower_options['fatigue_material_factor']
tower_options[:, 15] = 10000000  # General_Inputs(D38) #tower_options['del_nref']
tower_options[:, 16] = 2000000 # Details category Library(C26) #tower_options['n_weld']
tower_options[:, 17] = 3 # Details category Library(F26) #tower_options['m1_weld']
tower_options[:, 18] = 5 # Details category Library(G26) #tower_options['m2_weld']
tower_options[:, 19] = 12.16375752 # Details category Library(H26) #tower_options['loga1_weld']
tower_options[:, 20] = 15.8069492 # Details category Library(I26) #tower_options['loga2_weld']
tower_options[:, 21] = 2000000 # Details category Library(C27) #tower_options['n_bracket']
tower_options[:, 22] = 3 # Details category Library(F27) #tower_options['m1_bracket']
tower_options[:, 23] = 5 # Details category Library(G27) #tower_options['m2_bracket']
tower_options[:, 24] = 12.01029996  # Details category Library(H27) #tower_options['loga1_bracket']
tower_options[:, 25] = 15.55118659 # Details category Library(I27) #tower_options['loga2_bracket']
tower_options[:, 26] = 4 #  General_Inputs(D39) #tower_options['del_m']

column_header = "dc_weld, dc_bracket, calc_SCF_butt, calc_SCF_cone, calc_SCF_flange," + \
                "weld_prep_angle, weld_ground_flush, joint_type, max_misalignment, scf_additional," + \
                "quality_class, ue_max, thickness_exponent_weld, t_ref, fatigue_material_factor, del_nref," + \
                "n_weld, m1_weld, m2_weld, loga1_weld, loga2_weld, n_bracket,m1_bracket, m2_bracket,"	+ \
                "loga1_bracket, loga2_bracket, del_m"

np.savetxt(folder_path + '\\tower_options_script_input.csv', tower_options, delimiter=',', header= column_header, fmt = "%s", comments = '')

#np.savetxt('tower_options_script_input.csv', tower_options, fmt='%0.10f', delimiter=',', header= column_header)
#tower_cans[:, 0] = fetch_range_from_sheet(towergeo_sheet, "", "")
#difference_points[:,column_index] = diff_value_between_ranges(calculated_array, expected_array, 0)









#wb = xw.Book(r"E:\Work-tamal-bhai\fresh\tower_options_script_input.csv")
#
#print wb.sheets[0].range('A2:C2').value
#print wb.sheets[0].range('A2:C2').value[0]
#print type(wb.sheets[0].range('A2:C2').value[2])


#    
#tower_options = {}
##
#for index in range(1,  len(wb.sheets[0].range('A1:AA1')) + 1 ):
#    print wb.sheets[0].range((1,index), (2,index)).value
#    if(type(wb.sheets[0].range((1,index), (2,index)).value[0]) == type(wb.sheets[0].range((1,index), (2,index)).value[1])):
#        tower_options[str(wb.sheets[0].range((1,index), (2,index)).value[0])] = str.strip( str(wb.sheets[0].range((1,index), (2,index)).value[1]))
#    else:
#        tower_options[str(wb.sheets[0].range((1,index), (2,index)).value[0])] = float(wb.sheets[0].range((1,index), (2,index)).value[1])
#
#print tower_options
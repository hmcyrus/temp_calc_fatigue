# -*- coding: utf-8 -*-
"""
Created on Thu Mar 29 13:53:42 2018

@author: cyrus
"""
import numpy as np
import xlwings as xw

def fetch_range_from_sheet(xw_sheet, cell_begin, cell_end):
    return xw_sheet.range(cell_begin + ':' + cell_end).value


##### read sections
towergeo_sheet = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm").sheets['Towergeo']

number_of_sections = 5

tower_sections = np.zeros( shape = (number_of_sections, 3) )  # 3 information of section is required for fatigue calculation
tower_sections[:, 0] = fetch_range_from_sheet(towergeo_sheet, "B9", "B13")  #section_no	 B9:B13
tower_sections[:, 1] = fetch_range_from_sheet(towergeo_sheet, "E9", "E13")  #can_no_base	E9:E13
tower_sections[:, 2] = fetch_range_from_sheet(towergeo_sheet, "F9", "F13")  #can_no_top  F9:F13
column_header = "section_no, can_no_base, can_no_top"
np.savetxt('tower_sections_script_input.csv', tower_sections, fmt='%0.10f', delimiter=',', header= column_header)

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
np.savetxt('tower_cans_script_input.csv', tower_cans, fmt='%0.10f', delimiter=',', header= column_header)

##### read DEL_My_interpolated
f_loads_sheet = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm").sheets['F_Loads']
tower_del_my = np.zeros( shape = (number_of_cans + number_of_sections, 1) ) # here we fetch only one column

tower_del_my[:, 0] = fetch_range_from_sheet(f_loads_sheet, "K10", "K63")

column_header = "del_my"
np.savetxt('tower_cans_del_my_script_input.csv', tower_del_my, fmt='%0.10f', delimiter=',', header= column_header)

#tower_cans[:, 0] = fetch_range_from_sheet(towergeo_sheet, "", "")
#difference_points[:,column_index] = diff_value_between_ranges(calculated_array, expected_array, 0)


import numpy as np
import xlwings as xw

def fetch_range_from_sheet(xw_sheet, cell_begin, cell_end):
    return xw_sheet.range(cell_begin + ':' + cell_end).value

def diff_between_ranges(calculated_array, expected_array, if_print_arrays):
    if(if_print_arrays):
        print "found_array " + str(calculated_array)
        print "expected_array " + str(expected_array)
    assert len(calculated_array) == len(expected_array), "found_array and expected_array have different length"
    difference_array = np.zeros(len(calculated_array), dtype=float)    
    difference_array_percentage = np.zeros(len(calculated_array), dtype=float)
    for index in range(0, len(calculated_array)):
        difference_array[index] = expected_array[index] - calculated_array[index]        
        difference_array_percentage[index] = (difference_array[index]/expected_array[index])*100
    
    return [difference_array, difference_array_percentage]

def diff_value_between_ranges(calculated_array, expected_array, if_print_arrays):
    if(if_print_arrays):
        print "found_array " + str(calculated_array)
        print "expected_array " + str(expected_array)
    assert len(calculated_array) == len(expected_array), "found_array and expected_array have different length"
    difference_array = np.zeros(len(calculated_array), dtype=float)    
    for index in range(0, len(calculated_array)):
        difference_array[index] = expected_array[index] - calculated_array[index]        
    
    return difference_array

def diff_percentage_between_ranges(calculated_array, expected_array, if_print_arrays):
    if(if_print_arrays):
        print "found_array " + str(calculated_array)
        print "expected_array " + str(expected_array)
    assert len(calculated_array) == len(expected_array), "found_array and expected_array have different length"
    difference_array_percentage = np.zeros(len(calculated_array), dtype=float)
    for index in range(0, len(calculated_array)):
#        print expected_array[index]
        if(expected_array[index] != 0):
            difference_array_percentage[index] = ((expected_array[index] - calculated_array[index])/expected_array[index])*100
        else:
            difference_array_percentage[index] = expected_array[index] - calculated_array[index]        
    
    return difference_array_percentage

def test_diff_function():
    print diff_between_ranges([1,-2.5], [1, 5], 1)
    print diff_between_ranges([1,2.5], [1, 5], 1)
    print diff_between_ranges([1,2.5], [1, -5], 1)
    print diff_between_ranges([1,-2.5], [1, -5], 1)

def test_value_diff_function():
    print diff_value_between_ranges([1,-2.5], [1, 5], 1)
    print diff_value_between_ranges([1,2.5], [1, 5], 1)
    print diff_value_between_ranges([1,2.5], [1, -5], 1)
    print diff_value_between_ranges([1,-2.5], [1, -5], 1)

def test_percentage_diff_function():
    print diff_percentage_between_ranges([1,-2.5], [1, 5], 1)
    print diff_percentage_between_ranges([1,2.5], [1, 5], 1)
    print diff_percentage_between_ranges([1,2.5], [1, -5], 1)
    print diff_percentage_between_ranges([1,-2.5], [1, -5], 1)
    
def report_single_column(calculated_sheet, expected_sheet, calculated_begin_index, calculated_end_index, expected_begin_index, expected_end_index, difference_points, column_index):
    calculated_array = fetch_range_from_sheet(calculated_sheet, calculated_begin_index, calculated_end_index)
    expected_array = fetch_range_from_sheet(expected_sheet, expected_begin_index, expected_end_index)
    difference_points[:,column_index] = diff_value_between_ranges(calculated_array, expected_array, 0)
    column_index+=1
    difference_points[:,column_index] = diff_percentage_between_ranges(calculated_array, expected_array, 0)
    column_index+=1    
    return difference_points
    
#test_diff_function()
test_value_diff_function()
#test_percentage_diff_function()
    
#wb_target_excel = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm")
#wb_fatigue_output = xw.Book(r"E:\Work-tamal-bhai\fresh\tower_fatigue_output.csv")

calculated_sheet = xw.Book(r"E:\Work-tamal-bhai\fresh\tower_fatigue_output.csv").sheets[0]
expected_sheet = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm").sheets['Fatigue']

column_index = 0;
difference_points = np.zeros( shape = (54, 51) )
difference_points[:,column_index] = range(1,55)
print difference_points
column_index+=1
column_header = "number"

### Excel column C(z)
difference_points = report_single_column(calculated_sheet, expected_sheet, "A2", "A55", "C11", "C64", difference_points, column_index)
column_index += 2
column_header = ", z, z_percent"
### Excel column D(D)
difference_points = report_single_column(calculated_sheet, expected_sheet, "B2", "B55", "D11", "D64", difference_points, column_index)
column_index += 2
column_header = column_header + ", D, D_percent"
### Excel column E(t_below)
difference_points = report_single_column(calculated_sheet, expected_sheet, "C2", "C55", "E11", "E64", difference_points, column_index)
column_index += 2
column_header = column_header + ", t_below, t_below_percent"
### Excel column F(t_above)
difference_points = report_single_column(calculated_sheet, expected_sheet, "D2", "D55", "F11", "F64", difference_points, column_index)
column_index += 2
column_header = column_header + ", t_above, t_above_percent"
### Excel column G(W_below)
difference_points = report_single_column(calculated_sheet, expected_sheet, "E2", "E55", "G11", "G64", difference_points, column_index)
column_index += 2
column_header = column_header + ", W_below, W_below_percent"
### Excel column H(W_above)
difference_points = report_single_column(calculated_sheet, expected_sheet, "F2", "F55", "H11", "H64", difference_points, column_index)
column_index += 2
column_header = column_header + ", W_above, W_above_percent"
### Excel column S(Maximum misalignment from EN1991-1-6)
difference_points = report_single_column(calculated_sheet, expected_sheet, "G2", "G55", "S11", "S64", difference_points, column_index)
column_index += 2
column_header = column_header + ", Maximum misalignment, Maximum misalignment_percent"
### Excel column U(DEL_My)
difference_points = report_single_column(calculated_sheet, expected_sheet, "H2", "H55", "U11", "U64", difference_points, column_index)
column_index += 2
column_header = column_header + ", DEL_My , DEL_My_percent"
### Excel column V(ecc_thickness)
difference_points = report_single_column(calculated_sheet, expected_sheet, "I2", "I55", "V11", "V64", difference_points, column_index)
column_index += 2
column_header = column_header + ", ecc_thickness, ecc_thickness_percent"
### Excel column W(misalign_SN_inner)
difference_points = report_single_column(calculated_sheet, expected_sheet, "J2", "J55", "W11", "W64", difference_points, column_index)
column_index += 2
column_header = column_header + ", misalign_SN_inner, misalign_SN_inner_percent"
### Excel column X(misalign_SN_outer)
difference_points = report_single_column(calculated_sheet, expected_sheet, "K2", "K55", "X11", "X64", difference_points, column_index)
column_index += 2
column_header = column_header + ", misalign_SN_outer, misalign_SN_outer_percent"
### Excel column Y(SCF_butt_weld_outer)
difference_points = report_single_column(calculated_sheet, expected_sheet, "L2", "L55", "Y11", "Y64", difference_points, column_index)
column_index += 2
column_header = column_header + ", SCF_butt_weld_outer, SCF_butt_weld_outer_percent"
### Excel column Z(SCF_butt_weld_inner)
difference_points = report_single_column(calculated_sheet, expected_sheet, "M2", "M55", "Z11", "Z64", difference_points, column_index)
column_index += 2
column_header = column_header + ", SCF_butt_weld_inner, SCF_butt_weld_inner_percent"
### Excel column AB(SCF_cone_outer)
difference_points = report_single_column(calculated_sheet, expected_sheet, "N2", "N55", "AB11", "AB64", difference_points, column_index)
column_index += 2
column_header = column_header + ", SCF_cone_outer, SCF_cone_outer_percent"
### Excel column AC(SCF_cone_inner)
difference_points = report_single_column(calculated_sheet, expected_sheet, "O2", "O55", "AC11", "AC64", difference_points, column_index)
column_index += 2
column_header = column_header + ", SCF_cone_inner, SCF_cone_inner_percent"
### Excel column AD(total_SCF)
difference_points = report_single_column(calculated_sheet, expected_sheet, "P2", "P55", "AD11", "AD64", difference_points, column_index)
column_index += 2
column_header = column_header + ", total_SCF, total_SCF_percent"
### Excel column AJ(DES)
difference_points = report_single_column(calculated_sheet, expected_sheet, "Q2", "Q55", "AJ11", "AJ64", difference_points, column_index)
column_index += 2
column_header = column_header + ", DES, DES_percent"
### Excel column AM(thickness_factor)
difference_points = report_single_column(calculated_sheet, expected_sheet, "R2", "R55", "AM11", "AM64", difference_points, column_index)
column_index += 2
column_header = column_header + ", thickness_factor, thickness_factor_percent"
### Excel column AN(sigma_ref_EN_weld_factored)
difference_points = report_single_column(calculated_sheet, expected_sheet, "S2", "S55", "AN11", "AN64", difference_points, column_index)
column_index += 2
column_header = column_header + ", sigma_ref_EN_weld_factored, sigma_ref_EN_weld_factored_percent"
### Excel column AO(N_allow_weld)
difference_points = report_single_column(calculated_sheet, expected_sheet, "T2", "T55", "AO11", "AO64", difference_points, column_index)
column_index += 2
column_header = column_header + ", N_allow_weld, N_allow_weld_percent"
### Excel column AP(damage_weld)
difference_points = report_single_column(calculated_sheet, expected_sheet, "U2", "U55", "AP11", "AP64", difference_points, column_index)
column_index += 2
column_header = column_header + ", damage_weld, damage_weld_percent"
### Excel column AQ(DEL_margin_fatigue_weld)
difference_points = report_single_column(calculated_sheet, expected_sheet, "V2", "V55", "AQ11", "AQ64", difference_points, column_index)
column_index += 2
column_header = column_header + ", DEL_margin_fatigue_weld, DEL_margin_fatigue_weld_percent"
### Excel column AS(N_allow_brackets)
difference_points = report_single_column(calculated_sheet, expected_sheet, "W2", "W55", "AS11", "AS64", difference_points, column_index)
column_index += 2
column_header = column_header + ", N_allow_brackets, N_allow_brackets_percent"
### Excel column AT(damage_brackets)
difference_points = report_single_column(calculated_sheet, expected_sheet, "X2", "X55", "AT11", "AT64", difference_points, column_index)
column_index += 2
column_header = column_header + ", damage_brackets, damage_brackets_percent"
### Excel column AU(DEL_margin_fatigue_brackets)
difference_points = report_single_column(calculated_sheet, expected_sheet, "Y2", "Y55", "AU11", "AU64", difference_points, column_index)
column_index += 2
column_header = column_header + ", DEL_margin_fatigue_brackets, DEL_margin_fatigue_brackets_percent"

			
np.savetxt('fatigue_report.csv', difference_points, delimiter=',', header= column_header)

### Excel column ()
#difference_points = report_single_column(calculated_sheet, expected_sheet, "2", "55", "11", "64", difference_points, column_index)
#column_index += 2
#column_header = column_header + ", , _percent"



#des_array  = fatigue_sheet.range('AJ11:AJ64').value
#difference_points = np.zeros( shape = (len(des_array), 7) )

#print fetch_range_from_sheet(expected_sheet, "C11", "C64")  #C11:C64
#print fetch_range_from_sheet(calculated_sheet, "A2", "A55")  #A2:A55
#diff_between_ranges(fetch_range_from_sheet(calculated_sheet, "A2", "A55"), fetch_range_from_sheet(expected_sheet, "C11", "C64"), 0)

#calculated_array = fetch_range_from_sheet(calculated_sheet, "A2", "A55")
#expected_array = fetch_range_from_sheet(expected_sheet, "C11", "C64")
#difference_points[:,column_index] = diff_value_between_ranges(calculated_array, expected_array, 0)
#column_index+=1
#difference_points[:,column_index] = diff_value_between_ranges(calculated_array, expected_array, 0)
#column_index+=1
#print "column_index " + str(column_index) 
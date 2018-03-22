# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 18:09:58 2018

@author: cyrus
"""
import numpy as np
import xlwings as xw

wb = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm")
fatigue_sheet = wb.sheets['Fatigue']

des_array  = fatigue_sheet.range('AJ11:AJ64').value
difference_points = np.zeros( shape = (len(des_array), 7) )
difference_points[:,0] = range(1,55)

######### calculation for n_allowable_weld

des_array  = fatigue_sheet.range('AJ11:AJ64').value
sigma_ref_weld_factored_array  = fatigue_sheet.range('AN11:AN64').value
del_m = 4.
n_allowable_weld_array_expected = fatigue_sheet.range('AO11:AO64').value
n_allowable_weld_array = np.zeros(len(sigma_ref_weld_factored_array))
diff_percent_array_n_allowable = np.zeros(len(sigma_ref_weld_factored_array))
diff_array_n_allowable = np.zeros(len(sigma_ref_weld_factored_array))
#len(sigma_ref_weld_factored_array)
for index in range(0, len(sigma_ref_weld_factored_array)):    
    n_allowable_weld_array[index] = 10**( np.log10(2e6) + del_m * (np.log10(sigma_ref_weld_factored_array[index]) - np.log10(des_array[index])) )
    diff_percent_array_n_allowable[index] = ((n_allowable_weld_array_expected[index] - n_allowable_weld_array[index]) / n_allowable_weld_array_expected[index])*100.0
    diff_array_n_allowable[index] = n_allowable_weld_array_expected[index] - n_allowable_weld_array[index]

print "maximum difference in n_allowable_weld value- " + str(max(diff_array_n_allowable, key=abs))
print "maximum difference in n_allowable_weld percentage- " + str(max(diff_percent_array_n_allowable, key=abs))

difference_points[:,1] = diff_percent_array_n_allowable

######### calculation for damage_weld

damage_array_expected = fatigue_sheet.range('AP11:AP64').value
damage_array = np.zeros(len(damage_array_expected))
diff_percent_array_damage = np.zeros(len(sigma_ref_weld_factored_array))
diff_array_damage = np.zeros(len(sigma_ref_weld_factored_array))
#print len(damage_array_expected)
del_nref = 10000000
for index in range(0, len(damage_array_expected)):    
    damage_array[index] = del_nref/n_allowable_weld_array[index]
    diff_array_damage[index] = damage_array_expected[index] - damage_array[index]
    diff_percent_array_damage[index] = ((damage_array_expected[index] - damage_array[index])/damage_array_expected[index])*100.0

print "maximum difference in damage_weld value- " + str(max(diff_array_damage, key=abs))
print "maximum difference in damage_weld percentage- " + str(max(diff_percent_array_damage, key=abs))

difference_points[:,2] = diff_percent_array_damage

######### calculation for DEL_margin_fatigue_weld

margin_array_expected = fatigue_sheet.range('AQ11:AQ64').value
margin_array = np.zeros(len(margin_array_expected))
diff_percent_array_margin = np.zeros(len(margin_array_expected))
diff_array_margin = np.zeros(len(margin_array_expected))
m1_weld = 3.

for index in range(0, len(margin_array_expected)):        
    margin_array[index] = ( ( 1 / ( damage_array[index] ** (1/ del_m ) ) ) - 1 ) * 100  
    diff_array_margin[index] = margin_array_expected[index] - margin_array[index]
    diff_percent_array_margin[index] = (( margin_array_expected[index] - margin_array[index] ) / margin_array_expected[index]) * 100.0
    if index == 2:
        print margin_array[index]
        print margin_array_expected[index]

print "maximum difference in DEL_margin_fatigue_weld value- " + str(max(diff_array_margin, key=abs))
print "maximum difference in DEL_margin_fatigue_weld percentage- " + str(max(diff_percent_array_margin, key=abs))

difference_points[:,3] = diff_percent_array_margin

########## calculation for N_allow_brackets

n_allowable_bracket_array_expected = fatigue_sheet.range('AS11:AS64').value
n_allowable_bracket_array = np.zeros(len(n_allowable_bracket_array_expected))
diff_percent_array_n_allowable_bracket = np.zeros(len(n_allowable_bracket_array_expected))
diff_array_n_allowable_bracket = np.zeros(len(n_allowable_bracket_array_expected))

loga1_bracket = 12.01029996
scf_additional = 1.
fatigue_material_factor = 1.265
n_bracket = 2000000

for index in range(0, len(n_allowable_bracket_array_expected)):        
    sigma_ref_bracket = 10**( ( loga1_bracket - np.log10(2e6) ) / 3. ) 
    sigma_ref_bracket_factored = sigma_ref_bracket / ( scf_additional * fatigue_material_factor )        
    n_allowable_bracket_array[index] = 10**( np.log10( n_bracket ) + del_m * ( np.log10(sigma_ref_bracket_factored) - np.log10(des_array[index]) ) ) 
    diff_array_n_allowable_bracket[index] = n_allowable_bracket_array_expected[index] - n_allowable_bracket_array[index]
    diff_percent_array_n_allowable_bracket[index] = ((n_allowable_bracket_array_expected[index] - n_allowable_bracket_array[index]) / n_allowable_bracket_array_expected[index]) *100.
    
print "maximum difference in N_allow_brackets value- " + str(max(diff_array_n_allowable_bracket, key=abs))
print "maximum difference in N_allow_brackets percentage- " + str(max(diff_percent_array_n_allowable_bracket, key=abs))

difference_points[:,4] = diff_percent_array_n_allowable_bracket
######### calculation for damage_brackets

damage_bracket_array_expected = fatigue_sheet.range('AT11:AT64').value
damage_bracket_array = np.zeros(len(damage_array_expected))
diff_percent_array_damage_bracket = np.zeros(len(damage_bracket_array_expected))
diff_array_damage_bracket = np.zeros(len(damage_bracket_array_expected))
#print len(damage_array_expected)
del_nref = 10000000
for index in range(0, len(damage_bracket_array_expected)):    
    damage_bracket_array[index] = del_nref/n_allowable_bracket_array[index]
    diff_array_damage_bracket[index] = damage_bracket_array_expected[index] - damage_bracket_array[index]
    diff_percent_array_damage_bracket[index] = (( damage_bracket_array_expected[index] - damage_bracket_array[index]   )/damage_bracket_array_expected[index])*100.0

print "maximum difference in damage_brackets value- " + str(max(diff_array_damage_bracket, key=abs))
print "maximum difference in damage_brackets percentage- " + str(max(diff_percent_array_damage_bracket, key=abs))

difference_points[:,5] = diff_percent_array_damage_bracket
######### calculation for DEL_margin_fatigue_brackets

margin_bracket_array_expected = fatigue_sheet.range('AU11:AU64').value
margin_bracket_array = np.zeros(len(margin_bracket_array_expected))
diff_percent_array_margin_bracket = np.zeros(len(margin_bracket_array_expected))
diff_array_margin_bracket = np.zeros(len(margin_bracket_array_expected))

for index in range(0, len(margin_bracket_array_expected)):        
    margin_bracket_array[index] = ( ( 1 / ( damage_bracket_array[index] ** (1/ del_m ) ) ) - 1 ) * 100  
    diff_array_margin_bracket[index] = margin_bracket_array_expected[index] - margin_bracket_array[index]
    diff_percent_array_margin_bracket[index] = (( margin_bracket_array_expected[index] - margin_bracket_array[index] ) / margin_bracket_array_expected[index])*100.0

print "maximum difference in DEL_margin_fatigue_brackets value- " + str(max(diff_array_margin_bracket, key=abs))
print "maximum difference in DEL_margin_fatigue_brackets percentage- " + str(max(diff_percent_array_margin_bracket, key=abs))

difference_points[:,6] = diff_percent_array_margin_bracket

column_header = "weld_point_number, percentage_diff_n_allowable_weld, percentage_diff_damage_weld, percentage_diff_margin_weld, " + \
                    "percentage_diff_n_allowable_bracket, percentage_diff_damage_bracket, percentage_diff_margin_bracket"
np.savetxt('difference_report.csv', difference_points, delimiter=',', header= column_header)

#for index in rangde(0, len(diff_array_margin)):
#    print str(index) + " " + str(diff_array_margin[index])   
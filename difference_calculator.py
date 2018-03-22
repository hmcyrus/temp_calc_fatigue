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
sigma_ref_weld_factored_array  = fatigue_sheet.range('AN11:AN64').value
del_m = 4
n_allowable_weld_array_expected = fatigue_sheet.range('AO11:AO64').value
n_allowable_weld_array = np.zeros(len(sigma_ref_weld_factored_array))
diff_percent_array = np.zeros(len(sigma_ref_weld_factored_array))
diff_array = np.zeros(len(sigma_ref_weld_factored_array))
len(sigma_ref_weld_factored_array)
for index in range(0, len(sigma_ref_weld_factored_array)):    
    n_allowable_weld_array[index] = 10**( np.log10(2e6) + del_m * (np.log10(sigma_ref_weld_factored_array[index]) - np.log10(des_array[index])) )
    diff_percent_array[index] = (n_allowable_weld_array_expected[index] - n_allowable_weld_array[index]) / n_allowable_weld_array_expected[index]
    diff_array[index] = n_allowable_weld_array_expected[index] - n_allowable_weld_array[index]

print "maximum difference in value- " + str(max(diff_array))
print "maximum difference in percentage- " + str(max(diff_percent_array))
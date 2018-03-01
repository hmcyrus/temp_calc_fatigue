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
tower_fatigue_points = np.zeros( shape = (total_fatigue_points, 7) )

if os.path.isfile("tower_cans_del_my.csv"):
    print "reading del_my"

temp_del_my = np.genfromtxt('tower_cans_del_my.csv', delimiter=',', skip_header=1)
assert int(np.shape(temp_del_my)[0]) == total_fatigue_points, "correct number of del_my"

print temp_del_my[5]

if os.path.isfile("tower_options.csv"):
    print "reading tower_options"

tower_options = np.genfromtxt('tower_options.csv', delimiter=',', skip_header=1, dtype='unicode')

print float(tower_options[8])
print float(tower_options[11])

print np.sqrt(4.0)

sigma_ref_en = 10 ** ( ( np.log10( 2000000 ) - 12.16375752 ) / 3 )
print sigma_ref_en
# temp[19] = sigma_ref_en / (temp[18] * float(tower_options[14]))


n_ref = 2000000
m1 = 3
loga1 = 12.164
mat_factor = 1.265
t_factor = 1.14869835499704

sigma_ref_en = 10 ** ( ( np.log10( n_ref ) - loga1 ) / m1 )
sigma_ref_en_factored = sigma_ref_en/(t_factor * mat_factor)
print "using 10base log     " + str(sigma_ref_en_factored) + " " + str(sigma_ref_en)

sigma_ref_en = 10 ** ( ( np.log10( n_ref ) - np.log10(loga1) ) / m1 )
sigma_ref_en_factored = sigma_ref_en/(t_factor * mat_factor)
print "using 10base log + log(loga)     " + str(sigma_ref_en_factored) + " " + str(sigma_ref_en)

sigma_ref_en = 10 ** ( ( np.log( n_ref ) - loga1 ) / m1 )
sigma_ref_en_factored = sigma_ref_en/(t_factor * mat_factor)
print "using natural log        " + str(sigma_ref_en_factored)

sigma_ref_en = 10 ** ( ( np.log( n_ref ) - np.log(loga1) ) / m1 )
sigma_ref_en_factored = sigma_ref_en/(t_factor * mat_factor)
print "using natural log + log(loga)        " + str(sigma_ref_en_factored) + " " + str(sigma_ref_en)

sigma_ref_bracket = 10 ** ( ( float( tower_options[24]) - np.log10(2e6) ) / 4)

sigma_ref_bracket_factored = sigma_ref_bracket / ( float( tower_options[9]) * float(tower_options[14]) )

n_allowable_bracket = 10**( np.log10( float( tower_options[21]) ) + ( 4 * sigma_ref_bracket_factored ) - ( 4 * 30.190133) )

print n_allowable_bracket







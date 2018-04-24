import xlwings as xw
import copy
import pandas as pd
import numpy as np

# DEFINITION OF READER / WRITERS
class ReadWrite(object):
    @staticmethod
    def read(rng):
        return rng.value

    @staticmethod
    def write(rng, value):
        rng.value = value

SingleValue = ReadWrite
List = ReadWrite

class VerticalNamedDict(ReadWrite):

    @staticmethod
    def read(rng):
        keys = rng.value
        assert type(keys[0]) == type(u''), 'keys must be strings'
        if not len(keys) == len(set(keys)): #if not unique keys
            duplicates = set([x for x in keys if keys.count(x) > 1])
            raise Exception('keys must be unique, duplicates found ({})'.format(list(duplicates)))
        values = rng.offset(column_offset=1).value
        return dict(zip(keys,values)) #TODo consider ordered dict

    @staticmethod
    def write(rng,value):
        assert type(value) == type({})
        d = value
        keys = rng.value
        values = [d[key] for key in keys]
        rng.offset(column_offset=1).value = values

class TransposedNamedTableToRecords(ReadWrite):
    '''table that starts with a column of 'header names', and the body of values right of that '''

    @staticmethod
    def read(rng):
        table = rng.expand('right').value
        header = [l[0] for l in table]
        body = [l[1:] for l in table]
        records = []
        for i in range(len(body[0])): # for no. of items in table
            record = {k:l[i] for k, l in zip(header,body)}
            records.append(record)
        return records

    @staticmethod
    def write(rng, value):
        records = value
        orig_table = rng.value
        header = [l[0] for l in orig_table]
        table = [[s] + [x[s] for x in records] for s in header] #TODO: not tested yet...
        rng.value = table

class NamedTableToRecords(ReadWrite):
    '''table that starts with a column of 'header names', and the body of values right of that '''

    @staticmethod
    def read(rng):
        table = rng.expand('down').value
        headers = [c for c in table[0]]
        body = [l for l in table[1:]]
        records = {}
        for header in headers:
            records.update({header: []})

        for l in body:
            for i, k in enumerate(l):
                records[headers[i]].append(l[i])

        return records

    @staticmethod
    def write(rng, dict):
        headers = rng.value

        table_rng = rng.offset(1, 0).expand('down')
        table_rng.clear_contents()
        table=[]
        for header in headers:
            list = dict[header]
            table.append(list)

        table_trans = zip(*table)
        table_rng.value = table_trans


class NamedTableFromListOfInstances(ReadWrite):

    @staticmethod
    def read(rng):
        raise NotImplementedError()

    @staticmethod
    def write(rng,instances):
        """
        :param rng: part of horizontal row in excel containing desired output names
        :param instances: list of instances
        """

        header = rng.value
        if type(header) is list:
            # multiple column output
            body = [[(getattr(instance ,name,'') if name else None) for name in header] for instance in instances]
        elif type(header) is str or type(header) is unicode:
            #single column output
            body = [[(getattr(instance ,header,'') if header else None)] for instance in instances]

        #write to excel
        rng.offset(row_offset=1).expand('down').clear_contents()
        rng.offset(row_offset=1).columns[0].value = body

class NamedTransposedTableFromListOfInstances(ReadWrite):

    @staticmethod
    def read(rng):
        raise NotImplementedError()

    @staticmethod
    def write(rng, instances):
        """
        :param rng: part of vertical column in excel containing desired output names
        :param instances: list of instances
        """

        header = rng.value
        if type(header) is list:
            if type(instances) is list:
                body = [[(getattr(instance, name, '') if name else None) for instance in instances] for name in header]
            else:
                body = [[(getattr(instances, name, '') if name else None)] for name in header]
        elif type(header) is str or type(header) is unicode:
            if type(instances) is list:
                body = [[(getattr(instance, header, '') if header else None)] for instance in instances]
            else:
                body = [[(getattr(instances, header, '')if header else None)]]

        # write to excel
        rng.offset(column_offset=1).expand('right').clear_contents()
        rng.offset(column_offset=1).rows[0].value = body

user_manual_inputs = { #in seperate dict since these will be written back from file
'general':   {'sheet': 'General_Inputs', 'range': 'general_inputs', 'writer': VerticalNamedDict},
'can_no':           {'sheet': 'Towergeo', 'range': 'towergeo.can_no', 'writer': List},
'can_length':       {'sheet': 'Towergeo', 'range': 'towergeo.can_length', 'writer': List},
'can_thickness':    {'sheet': 'Towergeo', 'range': 'towergeo.can_thickness', 'writer': List},
'preferred_plate_height': {'sheet': 'Towergeo', 'range': 'towergeo.preferred_plate_height', 'writer': List},
'section_number':       {'sheet': 'Towergeo', 'range': 'towergeo.section_no', 'writer': List},
'flange_base_can_no':{'sheet': 'Towergeo', 'range': 'towergeo.flange_base_can_no', 'writer': List},
'flange_top_can_no':{'sheet': 'Towergeo', 'range': 'towergeo.flange_top_can_no', 'writer': List},
'section_shape':    {'sheet': 'Towergeo', 'range': 'towergeo.section_shape', 'writer': List},
'section_base_D':   {'sheet': 'Towergeo', 'range': 'towergeo.section_base_D', 'writer': List},
'section_top_D':    {'sheet': 'Towergeo', 'range': 'towergeo.section_top_D', 'writer': List},
'fatigue.options': {'sheet': 'Fatigue',  'range': 'names.fatigue.options', 'writer': NamedTableToRecords},
'connection_inputs':{'sheet': 'Flange', 'range': 'names.flange.connection_inputs', 'writer': TransposedNamedTableToRecords},
'flange.fatigue_inputs':        {'sheet': 'Flange', 'range': 'names.flange.fatigue_inputs', 'writer': TransposedNamedTableToRecords},
'flange.size_inputs':   {'sheet': 'Flange', 'range':'names.flange.size_inputs', 'writer': TransposedNamedTableToRecords},
'flange.optimization_inputs':        {'sheet': 'Flange', 'range': 'names.flange.optimization_inputs', 'writer': TransposedNamedTableToRecords},
'flange.path_rainflow':   {'sheet': 'Flange', 'range':'flange.path_rainflow', 'writer': SingleValue},
'fload.DEL_input':   {'sheet': 'F_loads', 'range':'names.fload.DEL_input', 'writer': NamedTableToRecords},
'fload.RSM_input': {'sheet': 'F_loads', 'range': 'names.fload.RSM_input','writer': NamedTableToRecords},
'VIV.scenarios': {'sheet': 'VIV', 'range': 'names.VIV.scenarios','writer': TransposedNamedTableToRecords},
'VIV.hotspot_inputs': {'sheet': 'VIV', 'range': 'names.VIV.hotspot_inputs','writer': NamedTableToRecords}
}

formula_generated_inputs = {#in seperate dict since these will not be written back from file (that would overwrite formulae)
'E_Loads.table': {'sheet': 'E_Loads',  'range': 'names.eloads.table_input', 'writer': NamedTableToRecords},
'connection_inputs':{'sheet': 'Flange', 'range': 'names.flange.connection_inputs', 'writer': TransposedNamedTableToRecords},
'flange.fatigue_inputs':{'sheet': 'Flange', 'range': 'names.flange.fatigue_inputs', 'writer': TransposedNamedTableToRecords}}



user_manual_outputs = { #in seperate dict since these will be written back from file
'eloads.table_output':   {'sheet': 'E_loads', 'range': 'names.eloads.table_output', 'writer': VerticalNamedDict},
'fatigue.weld_geo':   {'sheet': 'Fatigue', 'range': 'names.fatigue.weld_geo', 'writer': NamedTableToRecords}}


report_outputs = { #in seperate dict since these will be written back from file
'project_information.output':   {'sheet': 'Project_information', 'range': 'project_information.output', 'writer': VerticalNamedDict}}

# from line #568 of interface.py
def parse_library(wb=None):
    ''' Table of detail catagory data from library sheet'''
    if wb is None:
        wb = xw.Book.caller()

    # Create libraries for individual tables
    DC = wb.sheets['Library'].range('library.DetailCatagories').options(pd.DataFrame, transpose=True, expand='vertical').value.to_dict()
    structural_bolts = wb.sheets['Library'].range('library.structuralbolts').options(pd.DataFrame, transpose=True, expand='vertical').value.to_dict()
    # DIN_socket = wb.sheets['Library'].range('library.DIN_socket').options(pd.DataFrame, transpose=False,expand='vertical', header=True, index=False).value.to_dict(outtype='records')
    tower_materials = wb.sheets['Library'].range('library.materials').options(pd.DataFrame, transpose=False, expand='vertical', header=True, index=False).value # TODO: Convert to dictionary?
    can_plate_stock = wb.sheets['Towergeo'].range('library.can_plate_stock').options(pd.DataFrame, transpose=False,expand='vertical', header=True, index=False).value  # TODO: Convert to dictionary?
    buckling_kappa = wb.sheets['Library'].range('library.buckling_kappa').options(pd.DataFrame, transpose=False,expand='vertical', header=True,index=False).value
    buckling_kappa[buckling_kappa==999] = np.NaN
    DIN_socket = {}
    # Place individual libraries into single library for tower
    tower_library = {"DC": DC,
                    "structural_bolts": structural_bolts,
                    "DIN_socket": DIN_socket,
                    "materials": tower_materials,
                    "can_plate_stock": can_plate_stock,
                    "buckling_kappa": buckling_kappa}

    return tower_library

# from line #200 of parsing.py
# DEFINITION OF PARSING FUNCTIONS
def read_inputs(wb):

    mapping = copy.copy(user_manual_inputs)
    mapping.update(formula_generated_inputs)

    # create dict that contains inputs as defined in mappings above
    inputs = {}
    for key, pars in mapping.items():
        #print key
        rng = wb.sheets[pars['sheet']].range(pars['range'])
        inputs[key] = pars['writer'].read(rng)
        string = "range for inputs accessed as inputs[\"" + str(key) + "\"] collected from sheet " + pars['sheet'] + " is " + str(rng) + " \n"
        print string


    assert 1. <= inputs['general']['fatigue_material_factor'] < 2. , 'fatigue_material_factor {} not between 1 and 2'.format(inputs['general']['fatigue_material_factor'])

    # if False: # put condition here
    #     raise Exception('error message')
    # TODO add more input assertions here

    return inputs

wb = xw.Book(r"D:\tower_geo\project\Python_171106_Tower_v1.15_loads_iter6_set1_full_geo - Copy.xlsm")

inputs = read_inputs(wb)
# for key in inputs['general'].keys():
#     print key

# print inputs
# print inputs['general']
# print inputs[]

# import json
#
# with open('inputs_dictionary.json', 'w') as fp:
#     json.dump(inputs, fp)
# print inputs['E_Loads.table']
# print type(inputs['E_Loads.table'])
# print inputs['E_Loads.table']['Fxy']
# for key, value in inputs['E_Loads.table']:
#     print key
#     print inputs['E_Loads.table'][key]
    # if key == "Fxy":
    #     print key
    #     print inputs['E_Loads.table'][key]

# tower_materials = wb.sheets['Library'].range('library.materials').options(pd.DataFrame, transpose=False, expand='vertical', header=True, index=False).value # TODO: Convert to dictionary?'
# print tower_materials

# print(wb.sheets['Library'].range('library.materials'))
# print(wb.sheets['Library'].range('library.materials'))
# print parse_library(wb)
# library = parse_library(wb)
# print library["materials"]

# print "ranges that are read in parse_library"
#
# print "accessed as library[\"DC\"]"
# print wb.sheets['Library'].range('library.DetailCatagories')
# print "accessed as library[\"structural_bolts\"]"
# print wb.sheets['Library'].range('library.structuralbolts')
# print "accessed as library[\"DIN_socket\"]"
# print wb.sheets['Library'].range('library.DIN_socket')
# print "accessed as library[\"materials\"]"
# print wb.sheets['Library'].range('library.materials')
# print "accessed as library[\"can_plate_stock\"]"
# print wb.sheets['Towergeo'].range('library.can_plate_stock')
# print "accessed as library[\"buckling_kappa\"]"
# print wb.sheets['Library'].range('library.buckling_kappa')
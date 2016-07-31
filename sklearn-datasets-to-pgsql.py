#!/usr/bin/env python2.7

import numpy as np
import sklearn.datasets as ds
import re

def name_to_column(n):
    n = unicode(n)
    n = n.lower()
    n = re.sub(r'[^a-z0-9]', '_', n)
    n = re.sub(r'_+', '_', n)
    n = re.sub(r'_$', '', n)
    n = re.sub(r'^_', '', n)
    return n

def record_to_value(r):
    s = "("
    for c in r:
        if len(s) > 1:
            s = s + ", "
        s = s + str(c)
    s  = s + ")"
    return s

def get_target_names(d):
    cols = []
#    if 'target_names' in d:
#        for f in d['target_names']:
#            if re.search('^\d', name_to_column(f)) is not None:
#                cols.append("target_" + name_to_column(f))
#            else:
#                cols.append(name_to_column(f))
#    else:
    if len(np.shape(d['target'])) > 1:
        for i in range(0, np.shape(d['target'])[1]):
            cols.append('target_' + str(i))
    else:
        cols.append('target')
    return cols

def get_feature_names(d):
    cols = []
    if 'feature_names' in d:
        for f in d['feature_names']:
            cols.append(name_to_column(f))
    else:
        for i in range(0, np.shape(d['data'])[1]):
            cols.append('feature_' + str(i))
    return cols

def dataset_to_sql(table_name, d):
    print d

    data = np.c_[d['target'], d['data']]

    if 'target_names' in d:
        print "-- " + str(d['target_names'])

    colnames = get_target_names(d) + get_feature_names(d)
#    print(colnames)

    s = ""
    s2 = ""
    for c in colnames:
        if len(s) != 0:
            s = s + ", "
            s2 = s2 + ",\n"
        s = s + c
        s2 = s2 + "  " + c + " FLOAT NOT NULL"

    sql = "DROP TABLE IF EXISTS " + table_name + ";\n"
    sql = sql + "CREATE TABLE " + table_name + " (\n" + s2 + "\n);\n"

    sql = sql + "INSERT INTO " + table_name + " (" + s + ") VALUES\n"

    i = 0
    for dd in data:
        if i > 0:
            sql = sql + ",\n"
        sql = sql + "  " + record_to_value(dd)
        i += 1

    sql = sql + ";\n"
    return sql

print dataset_to_sql('boston', ds.load_boston())
print dataset_to_sql('iris', ds.load_iris())
print dataset_to_sql('diabetes', ds.load_diabetes())
print dataset_to_sql('digits', ds.load_digits())
print dataset_to_sql('linnerud', ds.load_linnerud())

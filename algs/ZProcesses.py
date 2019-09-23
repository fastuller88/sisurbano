# -*- coding: utf-8 -*-

"""
***************************************************************************
    densityPopulation.py
    ---------------------
    Date                 : July 2019
    Copyright            : (C) 2019 by Llactalab
    Email                : fastuller88 at gmail dot com
***************************************************************************
"""

__author__ = 'Johnatan Astudillo'
__date__ = 'July 2019'
__copyright__ = '(C) 2019, Llactalab'

from qgis.core import QgsProcessing
import processing


def joinAttrByLocation(input, inputJoin, fields, predicate,
                   discard, context, feedback,
                   output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}

    alg_params = {
        'DISCARD_NONMATCHING': discard,
        'INPUT': input,
        'JOIN': inputJoin,
        'JOIN_FIELDS': fields,
        'METHOD' : 1,
        'PREDICATE': predicate,  # 4:solapa, 0: Intesecta, 1: Contiene, 2: Iguala
        'OUTPUT': output
    }
    result = processing.run('qgis:joinattributesbylocation', alg_params,
                            context=context,
                            feedback=feedback, is_child_algorithm=True)
    return result


#  valuesFieldName = None : Se hace el conteo
def statisticsByCategories(input, categoriesFieldName,
                           valuesFieldName,
                           context, feedback,
                           output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'INPUT': input,
        'CATEGORIES_FIELD_NAME' : categoriesFieldName,
        'VALUES_FIELD_NAME' : valuesFieldName,
        'OUTPUT': output
    }
    result = processing.run('qgis:statisticsbycategories',
                            alg_params, context=context,
                            feedback=feedback, is_child_algorithm=True)

    return result

def joinAttrByNear(input,
                   input2, fieldsToCopy,
                   discard,
                   prefix,
                   maxDistance,
                   neighbors,
                   context, feedback,
                   output=QgsProcessing.TEMPORARY_OUTPUT):
    # Unir atributos por cercanía
    if feedback.isCanceled():
        return {}
    alg_params = {
        'DISCARD_NONMATCHING': discard,
        'FIELDS_TO_COPY': fieldsToCopy,
        'INPUT': input,
        'INPUT_2': input2,
        'MAX_DISTANCE' : maxDistance,
        'NEIGHBORS' : neighbors,
        'PREFIX': prefix,
        'OUTPUT': output
    }
    result = processing.run('native:joinbynearest',
                            alg_params, context=context,
                            feedback=feedback, is_child_algorithm=True)
    return result


def joinByAttr(input, field,
               input2, field2, fieldsToCopy,
               discard,
               prefix,
               context, feedback,
               output=QgsProcessing.TEMPORARY_OUTPUT):
    # Unir atributos por valor de campo
    if feedback.isCanceled():
        return {}
    alg_params = {
        'DISCARD_NONMATCHING': discard,
        'FIELD': field,
        'FIELDS_TO_COPY': fieldsToCopy,
        'FIELD_2': field2,
        'INPUT': input,
        'INPUT_2': input2,
        'METHOD': 1,
        'PREFIX': prefix,
        'OUTPUT': output
    }
    result = processing.run('native:joinattributestable',
                            alg_params, context=context,
                            feedback=feedback, is_child_algorithm=True)
    return result


def filter(input, field, operator, value, context, feedback,
           output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'FIELD': field,
        'INPUT': input,
        'METHOD': 0,
        'OPERATOR': operator,
        'VALUE': value,
        'OUTPUT': output
    }
    result = processing.run('qgis:selectbyattribute', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)

    # Extraer los objetos espaciales seleccionados
    alg_params = {
        'INPUT': result['OUTPUT'],
        'OUTPUT': output
    }
    result = processing.run('native:saveselectedfeatures', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)

    return result


def filterByExpression(input, expression, context, feedback,
                       output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    # Seleccionar por expresión
    alg_params = {
        'EXPRESSION': expression,
        'INPUT': input,
        'METHOD': 0
    }
    result = processing.run('qgis:selectbyexpression', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)
    # Extraer los objetos espaciales seleccionados
    alg_params = {
        'INPUT': result['OUTPUT'],
        'OUTPUT': output
    }
    result = processing.run('native:saveselectedfeatures', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)
    return result 


def createCentroids(input, context, feedback,
                    output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'ALL_PARTS': False,
        'INPUT': input,
        'OUTPUT': output
    }
    result = processing.run('native:centroids', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)
    return result


def createBuffer(input, distance, context, feedback,
                 output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'DISSOLVE': False,
        'DISTANCE': distance,
        'END_CAP_STYLE': 0,
        'JOIN_STYLE': 0,
        'MITER_LIMIT': 2,
        'SEGMENTS': 5,
        'INPUT': input,
        'OUTPUT': output
    }
    result = processing.run('native:buffer', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)

    return result


def calculateArea(input, field, context, feedback,
                  output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'FIELD_LENGTH': 16,
        'FIELD_NAME': field,
        'FIELD_PRECISION': 3,
        'FIELD_TYPE': 0,
        'FORMULA': ' $area ',
        'INPUT': input,
        'NEW_FIELD': True,
        'OUTPUT': output
    }
    result = processing.run('qgis:fieldcalculator', alg_params,
                            context=context, feedback=feedback,
                            is_child_algorithm=True)
    return result


def createGrid(input, cellSize, context, feedback,
               output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'CRS': 'ProjectCrs',
        'EXTENT': input,
        'HOVERLAY': 0,
        'HSPACING': cellSize,
        'TYPE': 4,
        'VOVERLAY': 0,
        'VSPACING': cellSize,
        'OUTPUT': output
    }
    result = processing.run('qgis:creategrid', alg_params, context=context,
                            feedback=feedback, is_child_algorithm=True)
    return result


def calculateField(input, field, formula, context, feedback,
                   output=QgsProcessing.TEMPORARY_OUTPUT, type=0):
    if feedback.isCanceled():
        return {}
    alg_params = {
        'FIELD_LENGTH': 10,
        'FIELD_NAME': field,
        'FIELD_PRECISION': 3,
        'FIELD_TYPE': type,
        'FORMULA': formula,
        'INPUT': input,
        'NEW_FIELD': True,
        'OUTPUT': output
    }
    result = processing.run('qgis:fieldcalculator', alg_params,
                            context=context,
                            feedback=feedback,
                            is_child_algorithm=True)
    return result


def intersection(input, inputOverlay,
                 inputFields, inputOverlayFields,
                 context, feedback,
                 output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}
    # validar que exista el campo pobacion
    alg_params = {
        'INPUT': input,
        'INPUT_FIELDS': inputFields,
        'OVERLAY': inputOverlay,
        'OVERLAY_FIELDS': inputOverlayFields,
        'OUTPUT': output
    }
    result = processing.run('native:intersection', alg_params,
                            context=context,
                            feedback=feedback,
                            is_child_algorithm=True)
    return result


def makeSureInside(input, context, feedback,
                   output=QgsProcessing.TEMPORARY_OUTPUT):
    # if feedback.isCanceled():
    #     return {}

    # alg_params = {
    #     'FIELD': ['id_grid'],
    #     'INPUT': input,
    #     'OUTPUT': output
    # }
    # result = processing.run('native:dissolve', alg_params,
    #                         context=context,
    #                         feedback=feedback,
    #                         is_child_algorithm=True)
    alg_params = {
        'DISSOLVE': False,
        'DISTANCE': -1,
        'END_CAP_STYLE': 0,
        'INPUT': input,
        'MITER_LIMIT': 2,
        'SEGMENTS': 5,
        'JOIN_STYLE': 0,
        'OUTPUT': output
    }
    result = processing.run('native:buffer', alg_params,
                            context=context,
                            feedback=feedback, is_child_algorithm=True)
    return result


def joinByLocation(input, inputJoin, fields, predicate, summaries,
                   discard, context, feedback,
                   output=QgsProcessing.TEMPORARY_OUTPUT):
    if feedback.isCanceled():
        return {}

    alg_params = {
        'DISCARD_NONMATCHING': discard,
        'INPUT': input,
        'JOIN': inputJoin,
        'JOIN_FIELDS': fields,
        'PREDICATE': predicate,  # 4:solapa, 0: Intesecta, 1: Contiene
        'SUMMARIES': summaries,  # 0:cuenta. 5: suma
        'OUTPUT': output
    }
    result = processing.run('qgis:joinbylocationsummary', alg_params,
                            context=context,
                            feedback=feedback, is_child_algorithm=True)
    return result
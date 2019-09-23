# -*- coding: utf-8 -*-

"""
/***************************************************************************
 Sisurbano
                                 A QGIS plugin
 Cáculo de indicadores urbanos
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-09-16
        copyright            : (C) 2019 by LlactaLAB
        email                : johnatan.astudillo@ucuenca.edu.ec
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Johnatan Astudillo'
__date__ = '2019-09-16'
__copyright__ = '(C) 2019 by LlactaLAB'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'

import os

from qgis.PyQt.QtCore import QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.core import (QgsProcessing,
                       QgsProcessingMultiStepFeedback,
                       QgsFeatureSink,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterFeatureSource,
                       QgsProcessingParameterField,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *
from .ZHelpers import *

pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class IC04Proximity2AlternativeTransport(QgsProcessingAlgorithm):
    """
    Mide el porcentaje de población que tiene acceso simultáneo a tres
    o más redes de transporte alternativo (bus, tranvía, bici pública,
    ciclovías, caminos peatonales). Se considera que la población tiene
    acceso a una red de transporte si su vivienda se encuentra dentro
    del área de influencia de dicha red, según lo siguiente: a 300m de
    una parada de bus urbano, 500m de una parada de tranvía, 300m de
    una estación de bici pública, 300m de ciclovías, y 300m de caminos
    peatonales.
    Formula: (Población cubierta por al menos 3 redes de transporte alternativo / Población total)*100

    Proximidad se define como viviendas ubicadas a:

    300m o menos de una parada de bus urbano, 
    500m o menos de una parada de tranvía,
    300m o menos de una estacíon de bici pública, 
    300m o menos de una ciclovía, 
    300m o menos de caminos peatonales    
    """

    BLOCKS = 'BLOCKS'
    FIELD_POPULATE_HOUSING = 'FIELD_POPULATE_HOUSING'
    CELL_SIZE = 'CELL_SIZE'    
    BUSSTOP = 'BUSSTOP'    
    TRAMSTOP = 'TRAMSTOP'    
    BIKESTOP = 'BIKESTOP'    
    BIKEWAY = 'BIKEWAY'    
    CROSSWALK = 'CROSSWALK'    
    OUTPUT = 'OUTPUT'



    def initAlgorithm(self, config):
        currentPath = getCurrentPath(self)
        FULL_PATH = buildFullPathName(currentPath, nameWithOuputExtension(NAMES_INDEX['IC04'][1]))           
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BLOCKS,
                self.tr('Manzanas'),
                [QgsProcessing.TypeVectorPolygon]
            )
        )

        self.addParameter(
            QgsProcessingParameterField(
                self.FIELD_POPULATE_HOUSING,
                self.tr('Población o viviendas'),
                'poblacion', 'BLOCKS'
            )
        )      
    

        self.addParameter(
            QgsProcessingParameterNumber(
                self.CELL_SIZE,
                self.tr('Tamaño de la malla'),
                QgsProcessingParameterNumber.Integer,
                P_CELL_SIZE, False, 1, 99999999
            )
        )        

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BUSSTOP,
                self.tr('Paradas de bus'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.TRAMSTOP,
                self.tr('Tranvía'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BIKESTOP,
                self.tr('Bici pública'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.BIKEWAY,
                self.tr('Ciclovía'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )

        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.CROSSWALK,
                self.tr('Caminos peatonales'),
                [QgsProcessing.TypeVectorAnyGeometry]
            )
        )                                

        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Salida'),
                QgsProcessing.TypeVectorAnyGeometry,
                str(FULL_PATH)                
            )
        )

    def processAlgorithm(self, params, context, feedback):
      steps = 0
      totalStpes = 37
      fieldPopulateOrHousing = params['FIELD_POPULATE_HOUSING']
      DISTANCE_BUSSTOP = 300
      DISTANCE_TRAMSTOP = 500
      DISTANCE_BKESTOP = 300
      DISTANCE_BIKEWAY = 300
      DISTANCE_CROSSWALK = 300


      feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)

      """
      -----------------------------------------------------------------
      Calcular las facilidades
      -----------------------------------------------------------------
      """

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksWithId = calculateField(params['BLOCKS'], 'id_block', '$id', context,
                                    feedback, type=1)

      steps = steps+1
      feedback.setCurrentStep(steps)
      centroidsBlocks = createCentroids(blocksWithId['OUTPUT'], context,
                                        feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blockBuffer4BusStop = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_BUSSTOP,
                                           context,
                                           feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blockBuffer4TramStop = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_TRAMSTOP, context,
                                        feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blockBuffer4BikeStop = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_BKESTOP, context,
                                         feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      BlockBuffer4BikeWay = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_BIKEWAY,
                                        context, feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      BlockBuffer4CrossWalk = createBuffer(centroidsBlocks['OUTPUT'], DISTANCE_CROSSWALK,
                                        context, feedback)    



      steps = steps+1
      feedback.setCurrentStep(steps)
      layerBusStop = calculateField(params['BUSSTOP'], 'idx', '$id', context,
                                    feedback, type=1)


      steps = steps+1
      feedback.setCurrentStep(steps)
      layerTramStop = calculateField(params['TRAMSTOP'], 'idx', '$id', context,
                                    feedback, type=1)    

      steps = steps+1
      feedback.setCurrentStep(steps)
      layerBikeStop = calculateField(params['BIKESTOP'], 'idx', '$id', context,
                                    feedback, type=1)       


      steps = steps+1
      feedback.setCurrentStep(steps)
      layerBikeWay = calculateField(params['BIKEWAY'], 'idx', '$id', context,
                                    feedback, type=1)   


      steps = steps+1
      feedback.setCurrentStep(steps)
      layerCrossWalk = calculateField(params['CROSSWALK'], 'idx', '$id', context,
                                    feedback, type=1)                                        


      layerBusStop = layerBusStop['OUTPUT']
      layerTramStop = layerTramStop['OUTPUT']
      layerBikeStop = layerBikeStop['OUTPUT']
      layerBikeWay = layerBikeWay['OUTPUT']
      layerCrossWalk = layerCrossWalk['OUTPUT']


      steps = steps+1
      feedback.setCurrentStep(steps)
      counterBusStop = joinByLocation(blockBuffer4BusStop['OUTPUT'],
                                        layerBusStop,
                                        'idx', [INTERSECTA], [COUNT],
                                        UNDISCARD_NONMATCHING,
                                        context,
                                        feedback)
      steps = steps+1
      feedback.setCurrentStep(steps)
      counterTramStop = joinByLocation(blockBuffer4TramStop['OUTPUT'],
                                     layerTramStop,
                                     'idx', [INTERSECTA], [COUNT],
                                     UNDISCARD_NONMATCHING,
                                     context,
                                     feedback)
      steps = steps+1
      feedback.setCurrentStep(steps)
      counteBikeStop = joinByLocation(blockBuffer4BikeStop['OUTPUT'],
                                      layerBikeStop,
                                      'idx', [INTERSECTA], [COUNT],
                                      UNDISCARD_NONMATCHING,
                                      context,
                                      feedback)
      steps = steps+1
      feedback.setCurrentStep(steps)
      counterBikeWay = joinByLocation(BlockBuffer4BikeWay['OUTPUT'],
                                    layerBikeWay,
                                    'idx', [INTERSECTA], [COUNT],
                                    UNDISCARD_NONMATCHING,
                                    context,
                                    feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      counterCrossWalk = joinByLocation(BlockBuffer4CrossWalk['OUTPUT'],
                                    layerCrossWalk,
                                    'idx', [INTERSECTA], [COUNT],
                                    UNDISCARD_NONMATCHING,
                                    context,
                                    feedback)    

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksJoined = joinByAttr(blocksWithId['OUTPUT'], 'id_block',
                                counterBusStop['OUTPUT'], 'id_block',
                                'idx_count',
                                UNDISCARD_NONMATCHING,
                                'bs_',
                                context,
                                feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                counterTramStop['OUTPUT'], 'id_block',
                                'idx_count',
                                UNDISCARD_NONMATCHING,
                                'ts_',
                                context,
                                feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                counteBikeStop['OUTPUT'], 'id_block',
                                'idx_count',
                                UNDISCARD_NONMATCHING,
                                'bks_',
                                context,
                                feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                counterBikeWay['OUTPUT'], 'id_block',
                                'idx_count',
                                UNDISCARD_NONMATCHING,
                                'bw_',
                                context,
                                feedback)


      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksJoined = joinByAttr(blocksJoined['OUTPUT'], 'id_block',
                                counterCrossWalk['OUTPUT'], 'id_block',
                                'idx_count',
                                UNDISCARD_NONMATCHING,
                                'cw_',
                                context,
                                feedback)    





      #FIXME: CAMBIAR POR UN METODO BUCLE

      formulaParseBS = 'CASE WHEN coalesce(bs_idx_count, 0) > 0 THEN 1 ELSE 0 END'
      formulaParseTS = 'CASE WHEN coalesce(ts_idx_count, 0) > 0 THEN 1 ELSE 0 END'
      formulaParseBKS = 'CASE WHEN coalesce(bks_idx_count, 0) > 0 THEN 1 ELSE 0 END'
      formulaParseBW = 'CASE WHEN coalesce(bw_idx_count, 0) > 0 THEN 1 ELSE 0 END'
      formulaParseCW = 'CASE WHEN coalesce(cw_idx_count, 0) > 0 THEN 1 ELSE 0 END'


      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksFacilities = calculateField(blocksJoined['OUTPUT'], 'parse_bs',
                                        formulaParseBS,
                                        context,
                                        feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksFacilities = calculateField(blocksFacilities['OUTPUT'], 'parse_ts',
                                        formulaParseTS,
                                        context,
                                        feedback)    


      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksFacilities = calculateField(blocksFacilities['OUTPUT'], 'parse_bks',
                                        formulaParseBKS,
                                        context,
                                        feedback)    


      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksFacilities = calculateField(blocksFacilities['OUTPUT'], 'parse_bw',
                                        formulaParseBW,
                                        context,
                                        feedback)  


      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksFacilities = calculateField(blocksFacilities['OUTPUT'], 'parse_cw',
                                        formulaParseCW,
                                        context,
                                        feedback)  


      formulaFacilities = 'parse_bs + parse_ts + parse_bks + parse_bw + parse_cw'


      steps = steps+1
      feedback.setCurrentStep(steps)
      blocksFacilities = calculateField(blocksFacilities['OUTPUT'], 'facilities',
                                        formulaFacilities,
                                        context,
                                        feedback)




      """
      -----------------------------------------------------------------
      Calcular numero de viviendas por hexagano
      -----------------------------------------------------------------
      """
      steps = steps+1
      feedback.setCurrentStep(steps)
      grid = createGrid(params['BLOCKS'], params['CELL_SIZE'], context,
                        feedback) 

      # Eliminar celdas efecto borde
      gridNeto = grid

      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNeto = calculateField(gridNeto['OUTPUT'], 'id_grid', '$id', context,
                                feedback, type=1)

      steps = steps+1
      feedback.setCurrentStep(steps)
      segments = intersection(blocksFacilities['OUTPUT'], gridNeto['OUTPUT'],
                              'bs_idx_count;ts_idx_count;bks_idx_count;bw_idx_count;cw_idx_count;facilities;' + fieldPopulateOrHousing,
                              'id_grid',
                              context, feedback)

      # Haciendo el buffer inverso aseguramos que los segmentos
      # quden dentro de la malla
      steps = steps+1
      feedback.setCurrentStep(steps)
      facilitiesForSegmentsFixed = makeSureInside(segments['OUTPUT'],
                                                  context,
                                                  feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNetoAndSegments = joinByLocation(gridNeto['OUTPUT'],
                                           facilitiesForSegmentsFixed['OUTPUT'],
                                           'bs_idx_count;ts_idx_count;bks_idx_count;bw_idx_count;cw_idx_count;facilities;' + fieldPopulateOrHousing,
                                           [CONTIENE], [MAX, SUM], DISCARD_NONMATCHING,                 
                                           context,
                                           feedback)

      # tomar solo los que tienen cercania simultanea (descartar lo menores de 3)
      MIN_FACILITIES = 3
      OPERATOR_GE = 3
      steps = steps+1
      feedback.setCurrentStep(steps)
      facilitiesNotNullForSegmentsFixed = filter(facilitiesForSegmentsFixed['OUTPUT'],
                                                 'facilities', OPERATOR_GE,
                                                 MIN_FACILITIES, context, feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      gridNetoAndSegmentsSimulta = joinByLocation(gridNeto['OUTPUT'],
                                                  facilitiesNotNullForSegmentsFixed['OUTPUT'],
                                                  fieldPopulateOrHousing,
                                                  [CONTIENE], [MAX, SUM], UNDISCARD_NONMATCHING,               
                                                  context,
                                                  feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      totalHousing = joinByAttr(gridNetoAndSegments['OUTPUT'], 'id_grid',
                                gridNetoAndSegmentsSimulta['OUTPUT'], 'id_grid',
                                fieldPopulateOrHousing+'_sum',
                                DISCARD_NONMATCHING,
                                'net_',
                                context,
                                feedback)

      steps = steps+1
      feedback.setCurrentStep(steps)
      formulaProximity = '(coalesce(net_'+fieldPopulateOrHousing+'_sum,0) /  coalesce('+fieldPopulateOrHousing+'_sum,0))*100'
      proximity2AlternativeTransport = calculateField(totalHousing['OUTPUT'], NAMES_INDEX['IC04'][0],
                                        formulaProximity,
                                        context,
                                        feedback, params['OUTPUT'])

      return proximity2AlternativeTransport




        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        #return {self.OUTPUT: dest_id}

    def icon(self):
        return QIcon(os.path.join(pluginPath, 'sisurbano', 'icons', 'green3.jpeg'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'C04 Proximidad a redes de transporte alternativo'

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'C Movilidad Urbana'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return IC04Proximity2AlternativeTransport()


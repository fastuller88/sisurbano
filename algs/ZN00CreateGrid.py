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
                       QgsProcessingParameterEnum,
                       QgsProcessingParameterFeatureSink)
from .ZProcesses import *
from .Zettings import *

#pluginPath = os.path.split(os.path.split(os.path.dirname(__file__))[0])[0]

class ZN00CreateGrid(QgsProcessingAlgorithm):
    """
    Distribuye la población de las manzanas a los puntos o medidores
    más cercanos al polígono de la manzana
    """  
    STUDY = 'STUDY'
    CELL_SIZE = 'CELL_SIZE' 
    OUTPUT = 'OUTPUT'

    def initAlgorithm(self, config):
        self.addParameter(
            QgsProcessingParameterFeatureSource(
                self.STUDY,
                self.tr('Área de estudio'),
                [QgsProcessing.TypeVectorPolygon]
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
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                self.tr('Salida')
            )
        )

    def processAlgorithm(self, params, context, feedback):
        steps = 0
        totalStpes = 4
        DISCARD = True
        UNDISCARD = False

        feedback = QgsProcessingMultiStepFeedback(totalStpes, feedback)    

        steps = steps+1
        feedback.setCurrentStep(steps)
        grid = createGrid(params['STUDY'], params['CELL_SIZE'], context,
                          feedback)

        gridNeto = grid

        # steps = steps+1
        # feedback.setCurrentStep(steps)
        # gridNeto = calculateArea(gridNeto['OUTPUT'], 'area_grid', context,
        #                          feedback)


        steps = steps+1
        feedback.setCurrentStep(steps)
        gridNeto = selectByLocation(gridNeto['OUTPUT'], params['STUDY'],
                                [INTERSECTA],
                                context, feedback, params['OUTPUT'])


        # steps = steps+1
        # feedback.setCurrentStep(steps)
        # gridNeto = calculateField(gridNeto['OUTPUT'], 'id_grid', '$id', context,
        #                           feedback, params['OUTPUT'], type=1)        


        return gridNeto

        # Return the results of the algorithm. In this case our only result is
        # the feature sink which contains the processed features, but some
        # algorithms may return multiple feature sinks, calculated numeric
        # statistics, etc. These should all be included in the returned
        # dictionary, with keys matching the feature corresponding parameter
        # or output names.
        #return {self.OUTPUT: dest_id}
                                          
    def icon(self):
        return QIcon(os.path.join(pluginPath, 'create_grid.png'))

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Z00 Crear malla'

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
        return 'Z General'

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return ZN00CreateGrid()

    def shortHelpString(self):
        return  "<b>Descripción:</b><br/>"\
                "<span>Crea una malla hexagonal en base a la extensión del área de estudio.</span>"

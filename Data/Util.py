import numpy as np
import math
from numpy.linalg import inv

class Util:
    def __init__(self, inWidth, inHeight, workImage, inputImage):
        self.inWidth = inWidth
        self.inHeight = inHeight
        self.cutContours = [[]] * 8
        self.workImage = workImage
        self.inputImage = inputImage
        
    def findStartAndEnd(self, contourPoints, targetPoint, startPoint, endPoint):
      w, h = targetPoint
      wStart, hStart = startPoint
      wEnd, hEnd = endPoint
    
      left = -1
      right = self.inWidth
      startIndex = -1
      endIndex = -1
    
      index90Degree = []
    
      for i in range(len(contourPoints)):
        point = contourPoints[i]
        wPoint, hPoint = point
    
        length1 = math.sqrt((hEnd - hStart) ** 2 + (wEnd - wStart) ** 2)
        length2 = math.sqrt((hPoint - h) ** 2 + (wPoint - w) ** 2)
        if length2 == 0:
          continue
        dotProduct = (hEnd - hStart) * (hPoint - h) + (wEnd - wStart) * (wPoint - w)
        angle = abs(np.arccos(dotProduct / length1 / length2))
        if abs(angle - math.pi / 2) < math.pi / 20:
          if startIndex == -1:
            startIndex = i
          else:
            endIndex = i
        else:
          if startIndex != -1 and endIndex != -1:
            index90Degree.append((startIndex, endIndex))
            startIndex = -1
            endIndex = -1
  
      # the 90 degree cut for left leg can include the right leg
      index90DegreeRefine = []
      left = -1
      right = self.inWidth
      index90DegreeLeft = -1, -1
      index90DegreeRight = -1, -1
      for pair in index90Degree:
        start2, end2 = pair
        ww, hh = contourPoints[start2]
        if ww < w and ww > left:
          left = contourPoints[start2][0]
          index90DegreeLeft = pair
        if ww > w and ww < right:
          right = contourPoints[start2][0]
          index90DegreeRight = pair
    
      index90DegreeRefine = [index90DegreeLeft, index90DegreeRight] if index90DegreeLeft[0] < index90DegreeRight[0] else [index90DegreeRight, index90DegreeLeft]
      return index90DegreeRefine
    
    def findElbowStartAndEnd(self, contourPoints, lineUpper, lineLower):
      pointShoulder, pointElbow = lineUpper
      _, pointHand = lineLower
      wPointShoulder, hPointShoulder = pointShoulder
      wPointElbow, hPointElbow = pointElbow
      wPointHand, hPointHand = pointHand
    
      left = -1
      right = self.inWidth
      startIndex = -1
      endIndex = -1
    
      indexHalfElbowAngle = []
      length1 = math.sqrt((hPointShoulder - hPointElbow) ** 2 + (wPointShoulder - wPointElbow) ** 2)
      length3 = math.sqrt((hPointHand - hPointElbow) ** 2 + (wPointHand - wPointElbow) ** 2)
      
      for i in range(len(contourPoints)):
        point = contourPoints[i]
        wPoint, hPoint = point
    
        length2 = math.sqrt((hPoint - hPointElbow) ** 2 + (wPoint - wPointElbow) ** 2)
        
        if length2 == 0:
          continue
        dotProduct2 = (hPointShoulder - hPointElbow) * (hPoint - hPointElbow) + (wPointShoulder - wPointElbow) * (wPoint - wPointElbow)
        angle2 = np.arccos(dotProduct2 / length1 / length2)
 
        
        dotProduct3 = (hPointHand - hPointElbow) * (hPoint - hPointElbow) + (wPointHand - wPointElbow) * (wPoint - wPointElbow)
        angle3 = np.arccos(dotProduct3 / length3 / length2)
        
        if abs(angle2 - angle3) < math.pi / 10:
          if startIndex == -1:
            startIndex = i
          else:
            endIndex = i
        else:
          if startIndex != -1 and endIndex != -1:
            indexHalfElbowAngle.append((startIndex, endIndex))
            startIndex = -1
            endIndex = -1
                   
      indexHalfElbowAngleRefine = []
          
      left = -1
      right = self.inWidth
      indexHalfElbowAngleLeft = -1, -1
      indexHalfElbowAngleRight = -1, -1
      for pair in indexHalfElbowAngle:
        start2, end2 = pair
        ww, hh = contourPoints[start2]
        if ww < wPointElbow and ww > left:
          left = contourPoints[start2][0]
          indexHalfElbowAngleLeft = pair
        if ww > wPointElbow and ww < right:
          right = contourPoints[start2][0]
          indexHalfElbowAngleRight = pair
    
      indexHalfElbowAngleRefine = [indexHalfElbowAngleLeft, indexHalfElbowAngleRight] if indexHalfElbowAngleLeft[0] < indexHalfElbowAngleRight[0] else [indexHalfElbowAngleRight, indexHalfElbowAngleLeft]
      return indexHalfElbowAngleRefine
        
    def findElbowStartAndEnd2(self, contourPoints, lineUpper, lineLower, rotateAngle, isLeft):
      pointShoulder, pointElbow = lineUpper
      _, pointHand = lineLower
      wPointShoulder, hPointShoulder = pointShoulder
      wPointElbow, hPointElbow = pointElbow
      wPointHand, hPointHand = pointHand
    
      left = -1
      right = self.inWidth
      startIndex = -1
      endIndex = -1
    
      indexHalfElbowAngle = []
      length1 = math.sqrt((hPointShoulder - hPointElbow) ** 2 + (wPointShoulder - wPointElbow) ** 2)
      length3 = math.sqrt((hPointHand - hPointElbow) ** 2 + (wPointHand - wPointElbow) ** 2)
      
      reverse = 1 if isLeft else -1
      for i in range(len(contourPoints)):
        point = contourPoints[i]
        wPoint, hPoint = point
    
        length2 = math.sqrt((hPoint - hPointElbow) ** 2 + (wPoint - wPointElbow) ** 2)
        
        if length2 == 0:
          continue
        dotProduct2 = (hPointShoulder - hPointElbow) * (hPoint - hPointElbow) + (wPointShoulder - wPointElbow) * (wPoint - wPointElbow)
        angle2 = np.arccos(dotProduct2 / length1 / length2)
 
        
        dotProduct3 = (hPointHand - hPointElbow) * (hPoint - hPointElbow) + (wPointHand - wPointElbow) * (wPoint - wPointElbow)
        angle3 = np.arccos(dotProduct3 / length3 / length2)
        
        if angle2 + angle3 > math.pi:
            if abs(angle2 - angle3 - rotateAngle * reverse) < math.pi / 10:
              if startIndex == -1:
                startIndex = i
              else:
                endIndex = i
            else:
              if startIndex != -1 and endIndex != -1:
                indexHalfElbowAngle.append((startIndex, endIndex))
                startIndex = -1
                endIndex = -1
        else:
            if abs(angle2 - angle3 + rotateAngle * reverse) < math.pi / 10:
              if startIndex == -1:
                startIndex = i
              else:
                endIndex = i
            else:
              if startIndex != -1 and endIndex != -1:
                indexHalfElbowAngle.append((startIndex, endIndex))
                startIndex = -1
                endIndex = -1           
                   
      indexHalfElbowAngleRefine = []
          
      left = -1
      right = self.inWidth
      indexHalfElbowAngleLeft = -1, -1
      indexHalfElbowAngleRight = -1, -1
      for pair in indexHalfElbowAngle:
        start2, end2 = pair
        ww, hh = contourPoints[start2]
        if ww < wPointElbow and ww > left:
          left = contourPoints[start2][0]
          indexHalfElbowAngleLeft = pair
        if ww > wPointElbow and ww < right:
          right = contourPoints[start2][0]
          indexHalfElbowAngleRight = pair
    
      indexHalfElbowAngleRefine = [indexHalfElbowAngleLeft, indexHalfElbowAngleRight] if indexHalfElbowAngleLeft[0] < indexHalfElbowAngleRight[0] else [indexHalfElbowAngleRight, indexHalfElbowAngleLeft]
      return indexHalfElbowAngleRefine
   
    def doMap(self, contourPoints, lineUpper, lineLower, angleUpper, angleLower, isLeft):
      indices = self.findElbowStartAndEnd(contourPoints, lineUpper, lineLower)
      indexM1 = indices[0][0]
      indexM2 = indices[1][0]
      pointM1 = contourPoints[indexM1]
      pointM2 = contourPoints[indexM2]
      
      shoulderPoint, elbowPoint = lineUpper
      _ , handPoint = lineLower
      indices2 = self.findStartAndEnd(contourPoints, shoulderPoint, shoulderPoint, elbowPoint)
      indexA = indices2[0][0]
      indexB = indices2[1][0]
      pointA = contourPoints[indexA]
      pointB = contourPoints[indexB]
      
      #construct upper contour
      contourUpper = []
      startPointCutContour = self.getInterpolatePoints(pointB, pointA)
      contourUpper.extend(startPointCutContour)
      
      pointM3 = self.rotatePoint(pointM1, elbowPoint, angleLower/2)
      pointM4 = self.rotatePoint(pointM2, elbowPoint, angleLower/2)
      pointM3Rotate = self.rotatePoint(pointM3, shoulderPoint, angleUpper)
      pointM4Rotate = self.rotatePoint(pointM4, shoulderPoint, angleUpper)
      
      inputControlPoints = [pointA, pointB, pointM1, pointM2]
      outputControlPoints = [pointA, pointB, pointM3Rotate, pointM4Rotate]
      for point in contourPoints[indexA: indexM1]:
          pointMap = self.findMapPoint(point, inputControlPoints, outputControlPoints)
          contourUpper.append(pointMap)

      elbowCutContour = self.getInterpolatePoints(pointM3Rotate, pointM4Rotate)
      contourUpper.extend(elbowCutContour)          

      for point in contourPoints[indexM2: indexB]:
          pointMap = self.findMapPoint(point, inputControlPoints, outputControlPoints)
          contourUpper.append(pointMap)      
 
      contourUpperRefine = []
      for i in range(0, len(contourUpper) - 1):
          for point in self.getInterpolatePoints(contourUpper[i], contourUpper[i+1]):
              contourUpperRefine.append(point)
              
      for point in self.getInterpolatePoints(contourUpper[-1], contourUpper[0]):
          contourUpperRefine.append(point)
              
      self.drawUpperContour(contourUpperRefine, outputControlPoints, inputControlPoints)
      #construct lower contour 
      contourLower = []
      elbowCutContour = self.getInterpolatePoints(pointM4Rotate, pointM3Rotate)
      contourLower.extend(elbowCutContour)  
      
      elbowPointRotate = self.rotatePoint(elbowPoint, shoulderPoint, angleUpper)
      handPointRotate1 = self.rotatePoint(handPoint, shoulderPoint, angleUpper)
      handPointRotate2 = self.rotatePoint(handPointRotate1, elbowPointRotate, angleLower)
      inputUpperControlPoints = [pointM1, pointM2, handPoint]
      outputUpperControlPoints = [pointM3Rotate, pointM4Rotate, handPointRotate2]
      
      for point in contourPoints[indexM1: indexM2]:
          pointMap = self.mapPoint(point, inputUpperControlPoints, outputUpperControlPoints)
          contourLower.append(pointMap) 
      
      contourLowerRefine = []
      for i in range(0, len(contourLower) - 1):
          for point in self.getInterpolatePoints(contourLower[i], contourLower[i+1]):
              contourLowerRefine.append(point)
              
      for point in self.getInterpolatePoints(contourLower[-1], contourLower[0]):
          contourLowerRefine.append(point)
          
      self.drawLowerContour(contourLowerRefine, outputUpperControlPoints, inputUpperControlPoints)  
      
      return contourUpperRefine, contourLowerRefine 
      
    def rotatePoint(self, point, center, angle):
        wCenter, hCenter = center
        w, h = point
        wRotate = int((w - wCenter) * math.cos(angle) - (h - hCenter) * math.sin(angle) + wCenter)
        hRotate = int((w - wCenter) * math.sin(angle) + (h - hCenter) * math.cos(angle) + hCenter)
        
        return (wRotate, hRotate)
        
    
    def drawUpperContour(self, contour, controlPointsOutput, controlPointsInput):
      hMin = self.inHeight
      hMax = -1
      for point in contour:
        w, h = point
        if h < hMin:
          hMin = h
        if h > hMax:
          hMax = h
    
      for h in range(hMin, hMax):
        wMin = self.inWidth
        wMax = -1
        for point in contour:
          w, h2 = point
          if h2 == h:
            if w < wMin:
              wMin = w
            if w > wMax:
              wMax = w
        for w in range(wMin, wMax):
          wInput, hInput = self.findMapPoint((w, h), controlPointsOutput, controlPointsInput)
          self.workImage[h, w] = self.inputImage[hInput, wInput]          
    
    def drawLowerContour(self, contour, controlPointsOutput, controlPointsInput):
      hMin = self.inHeight
      hMax = -1
      for point in contour:
        w, h = point
        if h < hMin:
          hMin = h
        if h > hMax:
          hMax = h
    
      for h in range(hMin, hMax):
        wMin = self.inWidth
        wMax = -1
        for point in contour:
          w, h2 = point
          if h2 == h:
            if w < wMin:
              wMin = w
            if w > wMax:
              wMax = w
        for w in range(wMin, wMax):
          wInput, hInput = self.mapPoint((w, h), controlPointsOutput, controlPointsInput)    
          self.workImage[h, w] = self.inputImage[hInput, wInput]     
          
    def getInterpolatePoints(self, pointStart, pointEnd):
      wStart, hStart = pointStart
      wEnd, hEnd = pointEnd
    
      points = []
    
      if abs(wStart - wEnd) > abs(hStart - hEnd):
        step =  1 if wStart < wEnd else -1
    
        for w in range(wStart, wEnd, step):
          k = (w - wStart) / (wEnd - wStart)
          h = round(hStart + k * (hEnd - hStart))
          points.append((w, h))
      else:
        step =  1 if hStart < hEnd else -1
    
        for h in range(hStart, hEnd, step):
          k = (h - hStart) / (hEnd - hStart)
          w = round(wStart + k * (wEnd - wStart))
          points.append((w, h))
    
      return points

    def getBodyContour(self, poseLines, contourPoints):
        def inInterval(target, start, end, length):
          if end - start < length / 2:
            return target > start and target < end
          else:
            return target > end or target < start

        intervals = []
        cutContours = []
        for poseLine in poseLines:
            pointPartStart, pointPartEnd = poseLine
            rangeStartAndEnd = self.findStartAndEnd(contourPoints, pointPartStart, pointPartStart, pointPartEnd)
            intervals.append((rangeStartAndEnd[0][0], rangeStartAndEnd[1][0]))
            cutContours.append(self.getInterpolatePoints(contourPoints[rangeStartAndEnd[0][0]], contourPoints[rangeStartAndEnd[1][0]]))
        
        trimmedBodyContour = []
        hasAddedParts = [False, False, False, False]
        for i in range(len(contourPoints)):
            isBody = True
            for j in range(len(hasAddedParts)):
                if inInterval(i, intervals[j][0], intervals[j][1], len(contourPoints)):
                    isBody = False
                    if not hasAddedParts[j]:
                        hasAddedParts[j] = True
                        trimmedBodyContour.extend(cutContours[j])
            if isBody:
                trimmedBodyContour.append(contourPoints[i])
             
        return trimmedBodyContour
    
    def mapPoint(self, point, controlPointsInput, controlPointsOutput):
        w, h = point
        w1Input, h1Input = controlPointsInput[0]
        w2Input, h2Input = controlPointsInput[1]
        w3Input, h3Input = controlPointsInput[2]
        w1Output, h1Output = controlPointsOutput[0]
        w2Output, h2Output = controlPointsOutput[1]
        w3Output, h3Output = controlPointsOutput[2]
        
        M = [[w1Input, w2Input, w3Input],
             [h1Input, h2Input, h3Input],
             [1, 1, 1]]
        MInv = inv(M)
        weights = np.matmul(MInv, [[w], [h], [1]])
        
        wMap = int(w1Output * weights[0][0] + w2Output * weights[1][0] + w3Output * weights[2][0])
        hMap = int(h1Output * weights[0][0] + h2Output * weights[1][0] + h3Output * weights[2][0])
        
        return wMap, hMap
    
    def findMapPoint(self, point, upperContourInput, upperContourOutput):
        #triangle1: startPointStart startPointEnd endPointStart
        #triangle2: endPointStart, endPointEnd startPointEnd
        #line: endPointStart startPointEnd
        startPointStart = upperContourInput[0]
        startPointEnd = upperContourInput[1]
        endPointStart = upperContourInput[2]
        #endPointEnd = upperContourInput[3]
        
        #line: ax + y + c = 0
        x1, y1 = startPointEnd
        x2, y2 = endPointStart
        a = (y2 - y1) / (x1 - x2)
        c = (y2 * x1 - y1 * x2) / (x2 - x1)
        x, y = point
        xStart, yStart = startPointStart
        startPointStartIsAbove = a * xStart + yStart + c 
        pointIsAbove = a * x + y + c 
        
        if startPointStartIsAbove * pointIsAbove > 0:
            controlPointsInput = [upperContourInput[0], upperContourInput[1], upperContourInput[2]]
            controlPointsOutput = [upperContourOutput[0], upperContourOutput[1], upperContourOutput[2]]
            return self.mapPoint(point, controlPointsInput, controlPointsOutput)
        else:
            controlPointsInput = [upperContourInput[1], upperContourInput[2], upperContourInput[3]]
            controlPointsOutput = [upperContourOutput[1], upperContourOutput[2], upperContourOutput[3]]
            return self.mapPoint(point, controlPointsInput, controlPointsOutput)
    
    def drawContour(self, contour, workImage, inputImage):
      hMin = self.inHeight
      hMax = -1
      for point in contour:
        w, h = point
        if h < hMin:
          hMin = h
        if h > hMax:
          hMax = h
    
      for h in range(hMin, hMax):
        wMin = self.inWidth
        wMax = -1
        for point in contour:
          w, h2 = point
          if h2 == h:
            if w < wMin:
              wMin = w
            if w > wMax:
              wMax = w
        for w in range(wMin, wMax):
          workImage[h, w] = inputImage[h, w]         

        
        
        
        
    
  
    
  
    
  
    
  
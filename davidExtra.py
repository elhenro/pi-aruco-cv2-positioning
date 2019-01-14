
  ...
  corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, dictionary, parameters=parameters)
  for i in range(0, len(ids)):
      marker = corners[i] 
      h,w = frame.shape[:2] # frame - original frame captured from camera
      newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, (w,h), 1, (w,h))
      undistortedMarker = cv2.undistortPoints(marker, cameraMatrix, distCoeffs, P=newCameraMatrix)

      print("Original %s:" % ids[i][0])
      print(marker)

      print('Undistorted %s:' % ids[i][0])
      print(undistortedMarker)

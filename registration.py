class Registration:

  def __init__(self, master, slave):
    self.master = master
    self.slave = slave
    self.shape = master.shape

  def rgb2gray(self, image):
    
    # OpenCv requires images with range between 0 and 255 and with uint8 type
    rescaled = (255.0/image.max()*(image - image.min())).astype(np.uint8)
    gray = cv2.cvtColor(rescaled, cv2.COLOR_RGB2GRAY)
    
    return gray

  def register(self, master, slave, registration_type = 'warp_affine'):
    master = rgb2gray(self.master)
    original_slave = slave
    slave = rgb2gray(self.slave)
    
    if registration_type == 'warp_perspective':
      orb_detector = cv2.ORB_create(9000)
      kp_master, d_master = orb_detector.detectAndCompute(master, None)
      kp_slave, d_slave = orb_detector.detectAndCompute(slave, None)

      matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)

      matches = matcher.match(d_master, d_slave)
      matches.sort(key=lambda x:x.distance)
      matches = matches[:int(len(matches)*90)]
      no_of_matches = len(matches)

      p1 = np.zeros((no_of_matches, 2))
      p2 = np.zeros((no_of_matches, 2))

      for i in range(no_of_matches):
        p1[i,:] = kp_master[matches[i].queryIdx].pt
        p2[i,:] = kp_slave[matches[i].trainIdx].pt

      homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)

      transformed = cv2.warpPerspective(original_slave, homography, (self.shape[0], self.shape[1]))
    elif registration_type == 'warp_affine':
      # Extract key points and SIFT description
      sift = cv2.xfeatures2d.SIFT_create()
      kp_master, d_master = sift.detectAndCompute(master, None)
      kp_slave, d_slave = sift.detectAndCompute(slave, None)
      
      # Extract positions of key points
      kp_master = np.array([p.pt for p in kp_master]).T
      kp_slave = np.array([p.pt for p in kp_slave]).T
      
      # Match descriptor and obtain two best matches
      matcher = cv2.BFMatcher()
      matches = matcher.knnMatch(d_master, d_slave, k = 2)
      
      # Initialize output variable
      fit_pos = np.array([], dtype=np.int32).reshape((0,2))
      
      no_of_matches = len(matches)
      for i in range(no_of_matches):
        # Obtain the good match if the ratio is smaller then 0.8
        if matches[i][0].distance <= 0.8*matches[i][1].distance:
          temp = np.array([matches[i][0].queryIdx, matches[i][0].trainIdx])
          fit_pos = np.vstack((fit_pos, temp))
      
      M = affine_matrix(kp_master, kp_slave, fit_pos)
      
      transformed = cv2.warpAffine(original_slave, M, (self.shape[0], self.shape[1]))
    
    return transformed
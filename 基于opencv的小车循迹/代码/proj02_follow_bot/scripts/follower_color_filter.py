#!/usr/bin/env python
# BEGIN ALL
import rospy, cv2, cv_bridge, numpy
from sensor_msgs.msg import Image

class Follower:
  def __init__(self):
    self.bridge = cv_bridge.CvBridge()
    self.image_sub = rospy.Subscriber('camera/rgb/image_raw', 
                                      Image, self.image_callback)
    self.ori_pub = rospy.Publisher('ori', Image, queue_size=1)
    self.hsv_pub = rospy.Publisher('hsv', Image, queue_size=1)
    self.mask_pub = rospy.Publisher('mask', Image, queue_size=1)
  def image_callback(self, msg):
    # BEGIN BRIDGE
    image = self.bridge.imgmsg_to_cv2(msg,desired_encoding='bgr8')
    self.ori_pub.publish(msg)
    # END BRIDGE
    # BEGIN HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    try:
       self.hsv_pub.publish(self.bridge.cv2_to_imgmsg(hsv))
    except cv_bridge.CvBridgeError as e:
       print(e)
    # END HSV
    # BEGIN FILTER
    lower_yellow = numpy.array([ 26,  43, 46])
    upper_yellow = numpy.array([34, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    # END FILTER
    masked = cv2.bitwise_and(image, image, mask=mask)
    try:
       self.mask_pub.publish(self.bridge.cv2_to_imgmsg(mask))
    except cv_bridge.CvBridgeError as e:
       print(e)
    cv2.waitKey(3)

rospy.init_node('follower')
follower = Follower()
rospy.spin()
# END ALL

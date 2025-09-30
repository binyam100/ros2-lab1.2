import math
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

class SquareNode(Node):
    def __init__(self):
        super().__init__('square_node')
        self.pub = self.create_publisher(Twist, 'turtle1/cmd_vel', 10)
        self.sub = self.create_subscription(Pose, 'turtle1/pose', self.on_pose, 10)
        self.timer = self.create_timer(0.05, self.on_tick)
        self.pose = None
        self.mode = 'FWD'
        self.start_x = None
        self.start_y = None
        self.start_th = None
        self.sides = 0
        self.v = 1.0
        self.w = 1.8

    def on_pose(self, p):
        self.pose = p

    def on_tick(self):
        if self.pose is None:
            return
        m = Twist()
        if self.mode == 'FWD':
            if self.start_x is None:
                self.start_x, self.start_y = self.pose.x, self.pose.y
            dx = self.pose.x - self.start_x
            dy = self.pose.y - self.start_y
            if (dx*dx + dy*dy) ** 0.5 >= 4.0:
                self.start_th = self.pose.theta
                self.mode = 'TURN'
            else:
                m.linear.x = self.v
        else:
            if self.start_th is None:
                self.start_th = self.pose.theta
            d = self._ang_diff(self.pose.theta, self.start_th)
            if abs(d) >= math.pi/2:
                self.sides += 1
                self.start_x = self.start_y = self.start_th = None
                if self.sides >= 4:
                    self.pub.publish(Twist())
                    self.timer.cancel()
                    return
                self.mode = 'FWD'
            else:
                m.angular.z = self.w
        self.pub.publish(m)

    @staticmethod
    def _ang_diff(a, b):
        d = a - b
        while d > math.pi:
            d -= 2*math.pi
        while d < -math.pi:
            d += 2*math.pi
        return d

def main(args=None):
    rclpy.init(args=args)
    n = SquareNode()
    try:
        rclpy.spin(n)
    except KeyboardInterrupt:
        pass
    finally:
        n.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

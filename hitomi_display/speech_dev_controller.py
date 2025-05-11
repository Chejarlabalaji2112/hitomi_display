import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import speech_recognition as sr

class VoiceCmdVel(Node):
    def __init__(self):
        super().__init__('voice_cmd_vel')
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.listening = False
        # Timer triggers every 2 seconds (adjust as needed)
        self.timer = self.create_timer(2.0, self.listen_and_publish)
        self.get_logger().info("VoiceCmdVel node started. Say a command...")

    def listen_and_publish(self):
        if self.listening:
            # Prevent overlapping listens
            return
        self.listening = True
        with self.microphone as source:
            self.get_logger().info("Listening for command...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            try:
                audio = self.recognizer.listen(source, timeout=5)
            except sr.WaitTimeoutError:
                self.get_logger().info("Listening timed out, no speech detected.")
                self.listening = False
                return
        try:
            command = self.recognizer.recognize_google(audio)
            self.get_logger().info(f"You said: {command}")
            self.publish_cmd(command.lower())
        except sr.UnknownValueError:
            self.get_logger().info("Sorry, I did not understand that.")
        except sr.RequestError as e:
            self.get_logger().error(f"Could not request results; {e}")
        self.listening = False

    def publish_cmd(self, command):
        twist = Twist()
        if 'forward' in command:
            twist.linear.x = 0.5
        elif 'backward' in command:
            twist.linear.x = -0.5
        elif 'left' in command:
            twist.angular.z = 1.0
        elif 'right' in command:
            twist.angular.z = -1.0
        elif 'stop' in command:
            twist.linear.x = 0.0
            twist.angular.z = 0.0
        else:
            self.get_logger().info("Unknown command.")
            return
        self.publisher.publish(twist)
        self.get_logger().info(f"Published: {command}")

def main(args=None):
    rclpy.init(args=args)
    node = VoiceCmdVel()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()

#Galura Lintang Dialog 23050874239
#Dewa Adi Baskara 23050874255
#Bintang Rahmansyah 23050874257

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import time
import math


class RectangleMoverNode(Node):
    def __init__(self):
        super().__init__('rectangle_mover')

        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 10)
        self.timer = self.create_timer(0.1, self.timer_callback)

        # Kecepatan
        self.linear_speed = 0.5    # m/s
        self.angular_speed = 0.5   # rad/s

        # Durasi tiap sisi (detik) -> sesuaikan supaya jadi persegi PANJANG
        # sisi panjang lebih lama waktunya daripada sisi pendek
        self.t_sisi_panjang = 6.0
        self.t_sisi_pendek = 3.0

        # Waktu untuk belok 90 derajat = (pi/2) / kecepatan_angular
        self.t_belok = (math.pi / 2) / self.angular_speed

        # Susun urutan gerakan: (jenis_gerak, durasi)
        # jenis_gerak: 'maju' atau 'belok'
        self.sequence = [
            ('maju', self.t_sisi_panjang),
            ('belok', self.t_belok),
            ('maju', self.t_sisi_pendek),
            ('belok', self.t_belok),
            ('maju', self.t_sisi_panjang),
            ('belok', self.t_belok),
            ('maju', self.t_sisi_pendek),
            ('belok', self.t_belok),
        ]

        self.current_index = 0
        self.state_start_time = time.time()

        self.get_logger().info('Mulai bergerak membentuk persegi panjang...')

    def timer_callback(self):
        msg = Twist()

        # Kalau semua tahap sudah selesai -> berhenti
        if self.current_index >= len(self.sequence):
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.publisher_.publish(msg)
            self.get_logger().info('Selesai! Robot sudah mengitari persegi panjang.')
            self.timer.cancel()
            rclpy.shutdown()
            return

        jenis, durasi = self.sequence[self.current_index]
        elapsed = time.time() - self.state_start_time

        if elapsed < durasi:
            if jenis == 'maju':
                msg.linear.x = self.linear_speed
                msg.angular.z = 0.0
                self.get_logger().info(f'Tahap {self.current_index + 1}: Maju...')
            elif jenis == 'belok':
                msg.linear.x = 0.0
                msg.angular.z = self.angular_speed
                self.get_logger().info(f'Tahap {self.current_index + 1}: Belok 90 derajat...')

            self.publisher_.publish(msg)
        else:
            # Pindah ke tahap berikutnya
            self.current_index += 1
            self.state_start_time = time.time()


def main(args=None):
    rclpy.init(args=args)
    node = RectangleMoverNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if rclpy.ok():
            node.destroy_node()
            rclpy.shutdown()


if __name__ == '__main__':
    main()


from typing import Tuple

# TODO sync exposure time between devices
import pyrealsense2 as rs

FPS = 15
WIDTH = 848
HEIGHT = 480


class Device:

    def __init__(self, pipeline: rs.pipeline, pipeline_profile: rs.pipeline_profile):
        self.pipeline = pipeline
        self.pipeline_profile = pipeline_profile


class DevicePair:
    def __init__(self, left: Device, right: Device):
        self.left = left
        self.right = right

    # return (left, right) , if new frames available, else None
    def poll_for_frames(self) -> (rs.composite_frame, rs.composite_frame):
        # wait for the left camera and poll the right?
        left = self.left.pipeline.poll_for_frames()
        right = self.right.pipeline.poll_for_frames()
        return (left, right) if left and right else None

    def wait_for_frames(self) -> tuple[rs.composite_frame, rs.composite_frame]:
        left = self.left.pipeline.wait_for_frames()
        right = self.right.pipeline.wait_for_frames()
        return left, right

    def stop(self):
        self.left.pipeline.stop()
        self.right.pipeline.stop()


def create_config():
    config = rs.config()
    # enable_stream(
    #   self: pyrealsense2.config,
    #   stream_type: pyrealsense2.stream,
    #   width: int,
    #   height: int,
    #   format: pyrealsense2.format=format.any,
    #   framerate: int=0) -> None
    # Infrared stream resolution is controlled by depth stream resolution
    config.enable_stream(rs.stream.infrared, 1, format=rs.format.y8, framerate=FPS)
    config.enable_stream(rs.stream.infrared, 2, format=rs.format.y8, framerate=FPS)
    config.enable_stream(rs.stream.depth, width=WIDTH, height=HEIGHT, format=rs.format.z16, framerate=FPS)
    # For now, we don't need color stream
    # config.enable_stream(rs.stream.color, width=WIDTH, height=HEIGHT, format=rs.format.rgb8, framerate=FPS)
    return config


class DeviceManager:

    def __init__(self, context: rs.context):
        self._context = context
        self._config_left = create_config()
        self._config_right = create_config()

    @staticmethod
    def enumerate_devices(context: rs.context):
        connected_devices = []

        for d in context.devices:
            if d.get_info(rs.camera_info.name).lower() != 'platform camera':
                serial = d.get_info(rs.camera_info.serial_number)
                product_line = d.get_info(rs.camera_info.product_line)
                name = d.get_info(rs.camera_info.name)
                device_info = {
                    "sn": serial,
                    "product_line": product_line,
                    "name": name
                }
                connected_devices.append(device_info)
        return connected_devices

    # return the serial numbers for left and right as tuple (left, right)
    @staticmethod
    def serial_selection():
        context = rs.context()
        devices = context.devices
        serials = list(map(lambda d: d.get_info(rs.camera_info.serial_number), devices))
        if len(serials) != 2:
            raise Exception(f"Unexpected number of devices (expected 2): {len(serials)}")
        for i in range(len(serials)):
            print(f"{i}: {serials[i]}")
        input_index = input(f"Input index of left camera serial number (facing the same direction as the camera): ")
        try:
            index_left = int(input_index)
            if index_left not in (0, 1):
                raise ValueError("Input must be 0 or 1")
        except ValueError as e:
            raise Exception(f"Invalid input: {e}")
        index_right = 0 if index_left == 1 else 1
        print(f"Selected devices:\n"
              f"Left Camera: {serials[index_left]}\n"
              f"Right Camera: {serials[index_right]}")
        return serials[index_left], serials[index_right]

    def enable_device(self, config, sn):
        pipeline = rs.pipeline(self._context)
        config.enable_device(sn)
        pipeline_profile = pipeline.start(config)
        return Device(pipeline, pipeline_profile)

    def enable_device_pair(self, sn_left, sn_right):
        left = self.enable_device(self._config_left, sn_left)
        right = self.enable_device(self._config_right, sn_right)
        return DevicePair(left, right)

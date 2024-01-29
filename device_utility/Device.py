import pyrealsense2 as rs


class Device:

    def __init__(self, device, serial):
        self.device: rs.device = device
        self.serial: str = serial
        self.config: rs.config = rs.config()
        self.config.enable_device(self.serial)
        self.pipeline: rs.pipeline = rs.pipeline()
        self.pipeline_profile: rs.pipeline_profile = None
        self.__is_streaming = False

    def is_streaming(self):
        return self.__is_streaming

    def start_stream(self, width=848, height=480, fps=15):
        self.config.enable_stream(rs.stream.depth, width=width, height=height, format=rs.format.z16, framerate=fps)
        self.config.enable_stream(rs.stream.infrared, 1, format=rs.format.y8, framerate=fps)
        self.config.enable_stream(rs.stream.infrared, 2, format=rs.format.y8, framerate=fps)
        self.pipeline_profile = self.pipeline.start(self.config)
        self.__is_streaming = True

    def stop_stream(self):
        self.pipeline.stop()
        self.__is_streaming = False

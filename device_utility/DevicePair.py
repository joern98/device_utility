import pyrealsense2 as rs

from device_utility.Device import Device


class DevicePair:
    def __init__(self, left: Device, right: Device):
        self.left = left
        self.right = right

    # return (left, right) , if new frames available, else None, THIS IS NOT WORKING PROPERLY
    def poll_for_frames(self) -> (rs.composite_frame, rs.composite_frame):
        # wait for the left camera and poll the right?
        left = self.left.pipeline.poll_for_frames()
        right = self.right.pipeline.poll_for_frames()
        return (left, right) if left and right else None

    def wait_for_frames(self) -> tuple[rs.composite_frame, rs.composite_frame]:
        left = self.left.pipeline.wait_for_frames()
        right = self.right.pipeline.wait_for_frames()
        return left, right

    def start(self, width=1280, height=720, fps=15, streams=(rs.stream.depth, rs.stream.infrared)):
        self.left.start_stream(width, height, fps, streams)
        self.right.start_stream(width, height, fps, streams)

    def stop(self):
        self.left.stop_stream()
        self.right.stop_stream()
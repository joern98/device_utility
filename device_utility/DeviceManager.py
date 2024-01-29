# TODO sync exposure time between devices
from typing import Dict, Any

import pyrealsense2 as rs

from device_utility.Device import Device
from device_utility.DevicePair import DevicePair

FPS = 15
WIDTH = 848
HEIGHT = 480


class DeviceManager:

    def __init__(self, context: rs.context):
        self._context = context

    @staticmethod
    def enumerate_devices(context: rs.context) -> dict[str, rs.device]:
        connected_devices: dict[str, rs.device] = {}

        for d in context.devices:
            if d.get_info(rs.camera_info.name).lower() != 'platform camera':
                serial = d.get_info(rs.camera_info.serial_number)
                connected_devices[serial] = d
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

    def create_device_pair(self, left_serial, right_serial):
        devices = self.enumerate_devices(self._context)
        left_device = devices[left_serial]
        right_device = devices[right_serial]
        left = Device(left_device, left_serial)
        right = Device(right_device, right_serial)
        return DevicePair(left, right)

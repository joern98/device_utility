import pyrealsense2 as rs


def set_sensor_option(sensor: rs.sensor, option: rs.option, value) -> bool:
    if sensor.supports(option):
        sensor.set_option(option, value)
        return True
    else:
        print(f"{sensor}, sn: {sensor.get_info(rs.camera_info.serial_number)} does not support option {option}!")
        return False


def get_sensor_option(sensor: rs.sensor, option: rs.option):
    if sensor.supports(option):
        value = sensor.get_option(option)
        return value
    else:
        print(f"{sensor}, sn: {sensor.get_info(rs.camera_info.serial_number)} does not support option {option}!")
        return None

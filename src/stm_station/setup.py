from setuptools import find_packages, setup
setup(name='stm_station', version='0.1.0', packages=find_packages(),
      data_files=[('share/ament_index/resource_index/packages', ['resource/stm_station']),
                  ('share/stm_station', ['package.xml'])],
      install_requires=['setuptools', 'pyserial'],
      maintainer='WinningLeos', maintainer_email='athens@todo.todo',
      description='STM serial bridge and controller', license='Proprietary',
      entry_points={'console_scripts': [
          'stm_serial_node = stm_station.serial_node:main',
          'stm_control_node = stm_station.control_node:main']})

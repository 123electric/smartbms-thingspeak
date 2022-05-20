import serial_asyncio
import time

BMS_COMM_GAP = 300
BMS_COMM_TIMEOUT = 10000
BMS_COMM_BLOCK_SIZE = 58

class BMS(object):
    def __init__(
        self,
        loop,
        port
    ):
        self._loop = loop
        self._serial_loop_task = None
        self._port = port
        self._last_received = 0
        self._pack_voltage = 0
        self._charge_current = 0
        self._discharge_current = 0
        self._pack_current = 0
        self._soc = 0
        self._lowest_cell_voltage = 0
        self._lowest_cell_voltage_num = 0
        self._highest_cell_voltage = 0
        self._highest_cell_voltage_num = 0
        self._lowest_cell_temperature = 0
        self._lowest_cell_temperature_num = 0
        self._highest_cell_temperature = 0
        self._highest_cell_temperature_num = 0
        self._cell_count = 0
        self._cell_communication_error = 1
        self._allowed_to_charge = 0
        self._allowed_to_discharge = 0

    async def connect(self):
        self._serial_loop_task = self._loop.create_task(self._serial_read(self._port))
    
    async def disconnect(self):
        self._serial_loop_task.cancel()

    @property
    def pack_voltage(self):
        return self._pack_voltage

    @property
    def charge_current(self):
        return self._charge_current

    @property
    def discharge_current(self):
        return self._discharge_current

    @property
    def pack_current(self):
        return self._pack_current

    @property
    def soc(self):
        return self._soc

    @property
    def lowest_cell_voltage(self):
        return self._lowest_cell_voltage

    @property
    def lowest_cell_voltage_num(self):
        return self._lowest_cell_voltage_num
    
    @property
    def highest_cell_voltage(self):
        return self._highest_cell_voltage

    @property
    def highest_cell_voltage_num(self):
        return self._highest_cell_voltage_num

    @property
    def lowest_cell_temperature(self):
        return self._lowest_cell_temperature

    @property
    def lowest_cell_temperature_num(self):
        return self._lowest_cell_temperature_num
    
    @property
    def highest_cell_temperature(self):
        return self._highest_cell_temperature

    @property
    def highest_cell_temperature_num(self):
        return self._highest_cell_temperature_num

    @property
    def cell_count(self):
        return self._cell_count

    @property
    def cell_communication_error(self):
        return self._cell_communication_error

    @property
    def serial_communication_error(self):
        if(self._millis() > self._last_received + BMS_COMM_TIMEOUT):
            return True
        else:
            return False

    @property
    def allowed_to_charge(self):
        return self._allowed_to_charge

    @property
    def allowed_to_discharge(self):
        return self._allowed_to_discharge

    async def _serial_read(self, port):
        reader, _ = await serial_asyncio.open_serial_connection(url=port, baudrate=9600)

        self._last_received = self._millis()
        bytes_received = 0
        buf = bytearray (BMS_COMM_BLOCK_SIZE)
        while True:
            rx_byte = await reader.readexactly(1)
            if self._millis() > self._last_received + BMS_COMM_GAP: 
                bytes_received = 0
            self._last_received = self._millis()

            if bytes_received <= BMS_COMM_BLOCK_SIZE-1:
                buf[bytes_received] = rx_byte[0]

            bytes_received += 1
       
            if bytes_received == BMS_COMM_BLOCK_SIZE:
                bytes_received = 0
                checksum = 0
                for i in range (BMS_COMM_BLOCK_SIZE-1):
                    checksum += buf[i]
                    
                received_checksum = buf[BMS_COMM_BLOCK_SIZE-1]
                if (checksum & 0xff) == received_checksum:
                    self._pack_voltage = self._decode_voltage(buf[0:3])
                    self._charge_current = self._decode_current(buf[3:6])
                    self._discharge_current = self._decode_current(buf[6:9])
                    self._pack_current = self._decode_current(buf[9:12])
                    self._soc = buf[40]
                    self._lowest_cell_voltage = self._decode_voltage(buf[12:14])
                    self._lowest_cell_voltage_num = buf[14]
                    self._highest_cell_voltage = self._decode_voltage(buf[15:17])
                    self._highest_cell_voltage_num = buf[17]
                    self._lowest_cell_temperature = self._decode_temperature(buf[18:20])
                    self._lowest_cell_temperature_num = buf[20]
                    self._highest_cell_temperature = self._decode_temperature(buf[21:23])
                    self._highest_cell_temperature_num = buf[23]
                    self._cell_count = buf[25]
                    self._cell_communication_error = True if (buf[30] & 0b00000100) else False
                    self._allowed_to_discharge = True if (buf[30] & 0b00000010) else False
                    self._allowed_to_charge = True if (buf[30] & 0b00000001) else False

    def _decode_current(self, raw_value):
        if raw_value[0] == ord('X'):
            return 0
        elif raw_value[0] == ord('-'):
            factor = -1
        else:
            factor = 1
        return factor*round(0.125*int.from_bytes(raw_value[1:3], byteorder='big', signed=False),1)

    def _decode_voltage(self, raw_value):
        #if(len(raw_value) == 3):
          #  voltage = int.from_bytes(raw_value[0:3], byteorder='big', signed=False)
        #else:
        voltage = int.from_bytes(raw_value, byteorder='big', signed=False) 
        return round(0.005*voltage,2)

    def _decode_temperature(self, raw_value):
        return round(int.from_bytes(raw_value[0:2], byteorder='big', signed=False)*0.857-232,0)
    
    def _millis(self):
        return int(time.time() * 1000)
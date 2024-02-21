import sys
from argparse import ArgumentParser
import asyncio
import aiohttp
from smartbms import BMS

class ComInstance:
    def __init__(
            self,
            port,
            key,
            bms
        ):
            self.port = port
            self.key = key
            self.bms = bms

async def program():
    tasks = []
    instances = []
    loop = asyncio.get_running_loop()
    print('123\\SmartBMS to Thingspeak\r\n')
    parser = ArgumentParser(description='123\\SmartBMS to Thingspeak')
    parser.add_argument('-p', '--port',nargs='+', help='Serial port(s). For multiple BMS, separate the ports with a space.')
    parser.add_argument('-k', '--key', nargs='+', help="Thingspeak channel key. For multiple BMS, separate the keys with a space.")
    args = parser.parse_args()

    if(args.port is None or args.key is None):
        print('At least one port and key are required as argument.')
        sys.exit()
        
    # In some cases, argparse does not split multiple values in one argument, so we have to do this manually
    ports = ' '.join(args.port).split(' ')
    keys = ' '.join(args.key).split(' ')
    
    for index, port in enumerate(ports):
        bms = BMS(loop, port)
        await bms.connect()
        com = ComInstance(port, keys[index], bms)
        instances.append(com)
    
    # sleep for 10 seconds so we have time to receive BMS data and for internet connection to start
    await asyncio.sleep(10)
    
    while(True):
        async with aiohttp.ClientSession() as session:
            try:
                # Customize the code below to the values you want to upload to Thingspeak.
                for instance in instances:
                    params = {
                        'field1': str(instance.bms.pack_voltage),
                        'field2': str(instance.bms.pack_current),
                        'field3': str(instance.bms.soc),
                        'field4': str(instance.bms.lowest_cell_voltage),
                        'field5': str(instance.bms.highest_cell_voltage),
                        'field6': str(int(instance.bms.allowed_to_charge)),
                        'field7': str(int(instance.bms.allowed_to_discharge)),
                        'field8': str(int(instance.bms.cell_communication_error or instance.bms.serial_communication_error))
                        }
                    params['api_key'] = instance.key
                    async with session.get('https://api.thingspeak.com/update', params=params) as resp:
                        if(resp.status == 200):
                            await resp.text()
                        elif(resp.status == 400):
                            print('Wrong Thingspeak key: {}'.format(instance.key))
                        else:
                            print('Error updating data: unknown error')
                
                print('Updated values')
            
            except Exception as e:
                print('Could not reach Thingspeak server: ', e)

        await asyncio.sleep(60)

def main():
    asyncio.run(program())

if __name__ == "__main__":
    main()


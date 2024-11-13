import struct

def SendStarCommand2uC(ser):
    BEGIN = str.encode('b')
    ser.write(BEGIN)


def SendStopCommand2uC(ser):
    STOP = str.encode('s')
    ser.write(STOP)


def SendParameters2uC(param, ser):
    PARAM = str.encode('p')
    ser.write(PARAM)
    data = struct.pack('!B', param.SetupVoltage >> 8)
    ser.write(data)
    data = struct.pack('!B', param.SetupVoltage & 255)
    ser.write(data)
    data = struct.pack('!B', param.SetupTime >> 8)
    ser.write(data)
    data = struct.pack('!B', param.SetupTime & 255)
    ser.write(data)
    data = struct.pack('!B', param.Signal)
    ser.write(data)
    data = struct.pack('!B', param.Vmax >> 8)
    ser.write(data)
    data = struct.pack('!B', param.Vmax & 255)
    ser.write(data)
    data = struct.pack('!B', param.Vmin >> 8)
    ser.write(data)
    data = struct.pack('!B', param.Vmin & 255)
    ser.write(data)
    data = struct.pack('!B', param.Slope >> 8)
    ser.write(data)
    data = struct.pack('!B', param.Slope & 255)
    ser.write(data)
    data = struct.pack('!B', param.Repetition)
    ser.write(data)


def ReadByteFromuC(ser):
    data = int.from_bytes(ser.read(1), "little")
    return data


def readPackageFromuC(ser, data_vec):
    # Read 32 bits sample identifier:
    data_vec[0] = (ReadByteFromuC(ser) << 24) + (ReadByteFromuC(ser) << 16) + (ReadByteFromuC(ser) << 8) + ReadByteFromuC(ser)
    # Read 16 bits Vre sample
    data_vec[1] = (ReadByteFromuC(ser) << 8) + ReadByteFromuC(ser)
    # Read 16 bits Vwe sample
    data_vec[2] = (ReadByteFromuC(ser) << 8) + ReadByteFromuC(ser)
    # Read 16 bits Vexc sample
    data_vec[3] = (ReadByteFromuC(ser) << 8) + ReadByteFromuC(ser)
    # Read 16 bits battery level
    # data_vec[4] = (ReadByteFromuC(ser) << 8) + ReadByteFromuC(ser)
    # Read Repetition
    data_vec[4] = ReadByteFromuC(ser)

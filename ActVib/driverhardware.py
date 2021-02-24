"""
  Driver Hardware
"""
import time
import serial
import struct

class driverhardware:

    def __init__(self, mwindow):
        self.mwindow = mwindow
        self.accscaler = 9.80665 * 2.0 / (2**15)
        self.gyroscaler = 250.0 / (2**15)
        self.accrangeselection = 0
        self.gyrorangeselection = 0
        self.filter = 0
        self.serial = None
        self.buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.accreadings = [0.0, 0.0, 0.0]  # x,y,z
        self.gyroreadings = [0.0, 0.0, 0.0]  # x,y,z
        self.dacout = [0, 0]
        self.gentipo = [0, 0]
        self.genamp = [0.0, 0.0]
        self.genfreq = [0.0, 0.0]
        self.chirpconf = [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]
        self.genConfigWritten = [False, False]
        self.setGeneratorConfig(id=0)
        self.setGeneratorConfig(id=1)
        self.serial = serial.Serial(port=None,
                                    baudrate=115200,
                                    parity=serial.PARITY_NONE,
                                    stopbits=serial.STOPBITS_ONE,
                                    bytesize=serial.EIGHTBITS,
                                    timeout=10)
        if self.serial.isOpen():
            self.serial.close()
        self.controlMode = False
        self.canalControle = 0
        self.ctrlalg = 0
        self.algon = False
        self.ctrlmem = 100
        self.ctrlmu = 0.1
        self.ctrlfi = 1e-4
        self.refid = 0
        self.erroid = 0
        self.packetsize = 17
        self.xref = 0
        self.xerro = 0
        self.algonchanged = False
        self.calctime = 0
        self.algontime = 0.0

    def openSerial(self):
        self.serial.port = self.mwindow.porta
        self.serial.open()

    def setGeneratorConfig(self, id=0, tipo=0, amp=0, freq=10, chirpconf=[0, 0, 0, 0, 0]):
        if tipo != 2:
            if (self.gentipo[id] != tipo) or (self.genamp[id] != amp) or (self.genfreq[id] != freq):
                self.genConfigWritten[id] = False
        else:
            self.chirpconf[id] = [int(chirpconf[0]), int(10 * chirpconf[1]),
                                  int(chirpconf[2]), int(10 * chirpconf[3]), int(chirpconf[4])]
        self.gentipo[id] = tipo
        self.genamp[id] = amp
        self.genfreq[id] = freq

    def setMPUFilter(self, nrange):
        self.filter = nrange

    def setMPUAddress(self, nrange):
        self.mpuaddress = nrange

    """ Seta range do acelerômetro:
        0 = -2 a +2 g
        1 = -4 a +4 g
        2 = -8 a +8 g
        3 = -16 a +16 g """
    def setAccRange(self, nrange):
        self.accrangeselection = nrange
        self.accscaler = 2.0**(nrange + 1) * 9.80665 / (2**15)

    """ Seta range do giroscópio:
        0 = -250 a +250 graus/s
        1 = -500 a +500 graus/s
        2 = -1000 a +1000 graus/s
        3 = -2000 a +2000 graus/s """
    def setGyroRange(self, nrange):
        self.gyrorangeselection = nrange
        self.gyroscaler = 250.0 * (2.0**nrange) / (2**15)

    def writeMPUScales(self):
        aux = 'c' + str(self.accrangeselection) + str(self.gyrorangeselection)
        self.serial.write(aux.encode())
        if self.serial.read(2) != b'ok':
            raise Exception('Config. de escalas sem resposta.')

    def initHardware(self):
        self.serial.write(b'i')
        if self.serial.read(3) != b'ok!':
            raise Exception('Falha de inicialização do MPU.')

    def writeMPUFilter(self):
        aux = 'g' + str(self.filter)
        self.serial.write(aux.encode())
        if self.serial.read(2) != b'ok':
            raise Exception('Config. de gerador sem resposta.')

    def writeGeneratorConfig(self, id=0):
        aux = 'G'
        aux = aux.encode() + bytes([id, self.gentipo[id], int(self.genamp[id]), int(self.genfreq[id])])
        aux = aux + bytes([int(round((self.genfreq[id] - int(self.genfreq[id])) * 100))])
        if self.gentipo[id] == 2:  # Chirp, manda mais 4 bytes [tinicio,deltai,tfim,deltaf]
            aux = aux + bytes(self.chirpconf[id])
        self.serial.write(aux)
        self.genConfigWritten[id] = True
        # if self.serial.read(3) != b'Oks':
        # raise Exception('Config. de filtro sem resposta.')

    def writeSensorChoice(self, id=-1):
        if (id == -1):
            aux = 'C'.encode() + bytes([self.mpuaddress])
        else:
            aux = 'C'.encode() + bytes([id])
        self.serial.write(aux)
        if self.serial.read(2) != b'ok':
            raise Exception('Erro na escolha do sensor.')

    def handshake(self):
        for k in range(5):
            self.serial.write(b'h')
            if self.serial.read(1) == b'k':
                return True
            self.serial.reset_output_buffer()
            self.serial.reset_input_buffer()
            time.sleep(0.1)
        raise Exception("Handshake com dispositivo falhou.")

    def setControlConfig(self, alg=0, mem=0, mu=0, fi=0, refid=0, erroid=0):
        self.ctrlalg = alg
        self.ctrlmem = mem
        self.ctrlmu = mu
        self.ctrlfi = fi
        self.refid = refid
        self.erroid = erroid

    def writeControlConfig(self):
        self.serial.write(b'!')
        self.buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.buf[0] = self.canalControle
        self.buf[1] = ((self.refid // 6) << 4) + (self.refid % 6)
        self.buf[2] = ((self.erroid // 6) << 4) + (self.erroid % 6)
        self.buf[3] = self.ctrlalg
        self.buf[4] = (self.ctrlmem >> 8) & 0xFF
        self.buf[5] = self.ctrlmem & 0xFF
        self.serial.write(bytearray(self.buf[0:6]))
        self.serial.write(bytearray(struct.pack("f", self.ctrlmu)))
        self.serial.write(bytearray(struct.pack("f", self.ctrlfi)))
        if self.serial.read(3) != b'ok!':
            raise Exception("Sem resposta gravando configurações de controle.")

    def setAlgOn(self, status=False, algontime=0.0, forcewrite=False):
        if (status != self.algon) or forcewrite:
            self.algontime = algontime
            self.algon = status
            self.algonchanged = True

    def writeAlgOn(self):
        if self.algon:
            # elf.serial.write(b'a\x01')
            self.serial.write(b'a\x02')
            self.serial.write(bytearray(struct.pack("f", self.ctrlmu)))
            self.serial.write(bytearray(struct.pack("f", self.ctrlfi)))
        else:
            self.serial.write(b'a\x00')
        self.algonchanged = False

    def startReadings(self):
        self.packetsize = 17
        self.serial.write(b's')
        if (len(self.serial.read(10)) < 10):
            raise Exception('Sem resposta nas leituras.')
        self.buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def startControl(self):
        self.packetsize = 14
        self.serial.write(b'S')
        if (len(self.serial.read(14)) < 14):
            raise Exception('Sem resposta nas leituras.')
        self.buf = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    def stopReadings(self):
        self.serial.write(b't')
        self.serial.flush()
        self.serial.close()

    def gravaFlash(self):
        self.serial.write(b'P')
        time.sleep(1.0)
        if self.serial.read(2) != b'ok':
            raise Exception("Sem resposta na gravação da flash.")

    def gravaCaminho(self, tipo, dados, pbar):
        BUFFER_SIZE = 64
        step = BUFFER_SIZE / 4
        pbar.setMaximum(dados.shape[0] - 2)
        pbar.setValue(0)
        npacotes = (dados.shape[0] * 4) // BUFFER_SIZE
        if ((dados.shape[0] * 4) % BUFFER_SIZE) > 0:
            pacoteextra = True
        else:
            pacoteextra = False
        self.serial.write(('W' + tipo).encode())
        self.serial.write(bytes([(dados.shape[0] * 4) >> 8, (dados.shape[0] * 4) & 0xFF]))
        if self.serial.read(1) == b'k':
            for k in range(npacotes):
                for w in dados[k * BUFFER_SIZE:k * BUFFER_SIZE + BUFFER_SIZE]:
                    self.serial.write(bytearray(struct.pack("f", w)))
                bb = self.serial.read(2)
                pbar.setValue(pbar.value() + (bb[0] << 8) + bb[1])
            if pacoteextra:
                for w in dados[npacotes * BUFFER_SIZE:]:
                    self.serial.write(bytearray(struct.pack("f", w)))
                buf = self.serial.read(2)
                pbar.setValue(pbar.value() + (bb[0] << 8) + bb[1])

    def getReading(self):
        ctaux = 0
        val = 0
        self.buf[0] = 0
        while not((self.buf[0] == 0xF) and (self.buf[1] == 0xF) and (self.buf[2] == 0xF)) and (ctaux < 64):
            self.buf[2] = self.buf[1]
            self.buf[1] = self.buf[0]
            self.buf[0] = (self.serial.read()[0])
            ctaux = ctaux + 1
        if ctaux == 64:
            raise Exception('Falha na leitura de pacote: cabeçalho não encontrado.')
        if self.controlMode:
            self.buf[0:13] = self.serial.read(13)[0:13]
            self.dacout[0] = self.buf[0]
            self.dacout[1] = self.buf[1]
            self.xref = struct.unpack("f", bytearray(self.buf[2:6]))[0]
            self.xerro = struct.unpack("f", bytearray(self.buf[6:10]))[0]
            self.calctime = (((self.buf[11] << 8) + self.buf[12]) << 4) / 240
        else:
            self.buf[0:16] = self.serial.read(16)[0:16]
            for k in range(3):
                bufa = self.buf[(2 * k):(2 * k + 2)]
                val = int((bufa[0] << 8) | bufa[1])
                val = val if ((bufa[0] >> 7) == 0) else (-1 * (65536 - val))
                self.accreadings[k] = float(val) * self.accscaler
            for k in range(3):
                bufa = self.buf[(2 * k + 8):(2 * k + 10)]
                val = int((bufa[0] << 8) | bufa[1])
                val = val if ((bufa[0] >> 7) == 0) else (-1 * (65536 - val))
                self.gyroreadings[k] = float(val) * self.gyroscaler
            self.dacout[0] = self.buf[14]
            self.dacout[1] = self.buf[15]

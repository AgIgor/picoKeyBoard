import time
import board
import digitalio
import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

cc = ConsumerControl(usb_hid.devices)
print(dir(board))

led = digitalio.DigitalInOut(board.LED)
led.switch_to_output()


# Configuração dos pinos do encoder
pin_a = board.GP2
pin_b = board.GP3
pin_mute = board.GP4

# Configuração dos objetos DigitalInOut para os pinos do encoder
encoder_pin_a = digitalio.DigitalInOut(pin_a)
encoder_pin_a.direction = digitalio.Direction.INPUT
encoder_pin_a.pull = digitalio.Pull.UP

encoder_pin_b = digitalio.DigitalInOut(pin_b)
encoder_pin_b.direction = digitalio.Direction.INPUT
encoder_pin_b.pull = digitalio.Pull.UP

b_pin_mute = digitalio.DigitalInOut(pin_mute)
b_pin_mute.direction = digitalio.Direction.INPUT
b_pin_mute.pull = digitalio.Pull.UP

# Inicialização de variáveis
contador = 0
estado_anterior_a = encoder_pin_a.value
estado_anterior_b = encoder_pin_b.value
estado_led = True

led.value = True 

# Loop principal
while True:
    # Leitura dos estados atuais dos pinos A e B
    estado_atual_a = encoder_pin_a.value
    estado_atual_b = encoder_pin_b.value
    
    if not b_pin_mute.value:
        print("Button mute!")
        cc.send(ConsumerControlCode.MUTE)
        time.sleep(0.5)
        estado_led = not estado_led

    # Verifica se houve uma transição no pino A
    if estado_atual_a != estado_anterior_a:
        # Verifica a direção do movimento do encoder
        if estado_atual_a == 0:
            if estado_atual_b == 0:
                
                contador += 1
                print("Volume up!")
                cc.send(ConsumerControlCode.VOLUME_INCREMENT)
                time.sleep(0.05)
                estado_led = not estado_led
                
            else:
                
                contador -= 1
                print("Volume down!")
                cc.send(ConsumerControlCode.VOLUME_DECREMENT)
                time.sleep(0.05)
                estado_led = not estado_led

    # Atualiza o estado anterior dos pinos
    estado_anterior_a = estado_atual_a
    estado_anterior_b = estado_atual_b
    
    led.value = estado_led
    
    # Aguarda um curto intervalo antes de realizar a próxima leitura
    time.sleep(0.01)

    # Exemplo: Imprime o valor do contador a cada segundo
    #if time.time() % 1 == 0:
        #print("Contador:", contador)


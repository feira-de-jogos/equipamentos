import time
from utils import initialize_state_file, get_ejection_state, set_ejection_state, get_product
from Stepper import MotorDePasso

initialize_state_file()

motor1 = MotorDePasso([26, 6, 13, 5], 400)
motor2 = MotorDePasso([21, 20, 16, 12], 400)
motor3 = MotorDePasso([1, 8, 7, 25], 400)

def eject_product(product_id):
    print(f"Ejetando produto com o ID: {}")

    
    if product_id == 1:
        motor1.girar_passos(400)

    elif product_id == 2:
        motor2.girar_passos(400)

    elif product_id == 3:
        motor3.girar_passos(400)
    

    set_ejection_state('s')
    print("Produto ejetado com sucesso!")


def update():
    while True:
        ejectionState = get_ejection_state()
        if ejectionState == 'w':
            print('Esperando...')
        elif ejectionState.startswith('p'):
            print('Processando...')
            productId = get_product()

            eject_product(productId)

        time.sleep(2.0)  # Espera 2 segundos entre as interações


# Chamando a função update para iniciar o loop
update()

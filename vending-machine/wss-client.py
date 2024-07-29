from os import getenv
from dotenv import load_dotenv
import asyncio
import socketio
import jwt
from stepper import Stepper

load_dotenv()
url = getenv("URL", default="wss://feira-de-jogos.dev.br")
socketio_path = getenv("SOCKETIO_PATH", default="/api/v2/machine")
namespace = getenv("NAMESPACE", default="/vending-machine")
jwt_algorithm = getenv("JWT_ALGORITHM", default="HS256")
secret_key = getenv("TOKEN_SECRET_KEY_VENDING_MACHINE", default="")


motores = []
motores.append(Stepper(pinos=[26, 6, 13, 5]))  # motor 1
motores.append(Stepper(pinos=[21, 20, 16, 12]))  # motor 2
motores.append(Stepper(pinos=[1, 8, 7, 25]))  # motor 3
sio = socketio.AsyncClient()


@sio.event(namespace=namespace)
async def connect():
    """
    Conexão ao servidor estabelecida
    """
    print("Conexão estabelecida")
    message = {"stateUpdate": {"state": "idle", "operation": 0}}
    await sio.emit(message, namespace=namespace)


@sio.event(namespace=namespace)
async def onStateMFA(req):
    """
    Recebe a solicitação para autenticação em duas etapas
    """
    username = req["username"]
    code = req["code"]
    operation = req["operation"]

    print("Olá, %s! Seu código de autenticação é %s." % (username, code))

    message = {"stateUpdate": {"state": "mfa", "operation": operation}}
    await sio.emit(message, namespace=namespace)


@sio.event(namespace=namespace)
async def onStateReleasing(req):
    """
    Recebe a solicitação para liberar o produto
    """
    product = req["product"]
    operation = req["operation"]

    message = {"stateUpdate": {"state": "releasing", "operation": operation}}
    await sio.emit(message, namespace=namespace)

    try:
        motores[product].girar_angulo(
            360, sentido_horario=True, tempo=0.008, modo="passo_completo"
        )
    finally:
        motores[product].desligar()

    message = {"stateUpdate": {"state": "idle", "operation": operation}}
    await sio.emit(message, namespace=namespace)


@sio.event(namespace=namespace)
async def disconnect():
    """
    Conexão ao servidor encerrada
    """
    print("Conexão encerrada")


async def main():
    """
    Função principal
    """
    message = {"machine": "vending-machine", "id": 0}
    token = jwt.encode(message, secret_key, algorithm=jwt_algorithm)
    await sio.connect(
        url,
        socketio_path=socketio_path,
        namespaces=namespace,
        auth={"token": token},
    )
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
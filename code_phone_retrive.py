import json
import time


from selenium.common import WebDriverException



def retrieve_phone_code(driver) -> str:
    """Esta función busca y devuelve el código de confirmación del teléfono.

    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación.

    Args:
        driver: Instancia del controlador web (WebDriver) donde se buscará el código de confirmación.

    Returns:
        str: El código de confirmación del teléfono como una cadena de dígitos.

    Raises:
        Exception: Si no se encuentra el código de confirmación después de 10 intentos.
    """
    global code
    for _ in range(10):  # Intentar 10 veces
        try:
            # Obtener los registros de rendimiento del navegador
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]

            # Iterar sobre los registros en orden inverso para buscar el último código de confirmación
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                # Obtener el cuerpo de la respuesta de la solicitud
                body = driver.execute_cdp_cmd('Network.getResponseBody', {'requestId': message_data["params"]["requestId"]})
                # Extraer los dígitos del cuerpo de la respuesta para encontrar el código de confirmación
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            # Manejar la excepción si hay un problema con el controlador web
            time.sleep(1)  # Esperar un segundo antes de reintentar
            continue

        if code:
            # Si se encuentra un código de confirmación, devolverlo
            return code

    # Si no se encuentra ningún código después de 10 intentos, generar una excepción
    raise Exception("No se encontró el código de confirmación del teléfono.\n"
                    "Utiliza 'retrieve_phone_code' solo después de haber solicitado el "
                    "código en tu aplicación.")


from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def enter_confirmation_code(driver, code):
    try:
        # Esperar hasta que el campo de entrada esté presente y sea interactivo
        confirmation_input = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//input[@id="code"]'))
        )

        # Limpiar el campo de entrada antes de escribir el código
        confirmation_input.clear()

        # Ingresar el código de confirmación en el campo de entrada
        confirmation_input.send_keys(code)

        print("Código de confirmación ingresado correctamente:", code)
    except Exception as e:
        print("Error al ingresar el código de confirmación:", e)
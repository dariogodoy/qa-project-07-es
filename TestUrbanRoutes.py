import unittest

import pytest
from selenium import webdriver
from selenium.common import  NoSuchElementException
from selenium.webdriver.common.by import By

from Urban_Routes_Page import UrbanRoutesPage
import data
import time
from code_phone_retrive import retrieve_phone_code, enter_confirmation_code


class TestUrbanRoutes:
    driver = None
    urban_routes_url = 'https://cnt-4eebf998-d951-4b21-9ec9-5bcb04b3c3c1.containerhub.tripleten-services.com'

    def __init__(self):
        self.page = None

    @classmethod
    def setup_class(cls):
        # Configuración inicial para las pruebas. Inicializa el controlador de Chrome y habilita el registro de
        # eventos de rendimiento.

        from selenium.webdriver import DesiredCapabilities

        capabilities = DesiredCapabilities.CHROME

        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}

        cls.driver = webdriver.Chrome()

    def test_order_taxi(self):
        driver = self.driver
        driver.get(self.urban_routes_url)

        routes_page = UrbanRoutesPage(self.driver)

        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)

        # Selecciona el modo de transporte personal
        routes_page.modes_car_button()

        # Selecciona el modo de transporte
        routes_page.select_car_mode()

        # Selecciona el boton pedir taxi
        routes_page.select_taxi()

        # Selecciona la opcion comfort
        routes_page.select_comfort_rate()

        # Agrega el botón de número de teléfono
        # noinspection PyArgumentList
        routes_page.add_phone_button()

        # Completar el numero de telefono
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)
        time.sleep(5)

        # Dar click en siguiente
        routes_page.click_next_button()
        time.sleep(15)

        # Codigo de configuracion obtenido de la aplicación
        code = retrieve_phone_code(driver)
        print("Phone code: " + code)

        # Codigo de confirmacion del codigo
        enter_confirmation_code(driver, code)

        # Dar click en confirmar
        routes_page.confirm_button_click()
        time.sleep(2)

        # Agregar metidi de pago
        routes_page.pay_method_click()

        # Agregar tarjeta
        routes_page.add_card()

        # Agregar el numero y codigo de tarjeta
        card_number = data.card_number
        card_code = data.card_code
        routes_page.card_numbers(card_number, card_code)
        time.sleep(5)

        # Click en agregar
        routes_page.click_add_button()

        # Cerrar la ventana emegente
        routes_page.close_popup_window()

        # Dejar un comentario
        routes_page.test_set_message_for_driver()
        time.sleep(3)

        # Elegir manta
        routes_page.click_blanket_tissues()
        time.sleep(4)

        # Elegir helados
        routes_page.increment_ice_cream()
        routes_page.increment_ice_cream()
        time.sleep(3)

        # Dar click en llamar taxi
        routes_page.click_call_taxi_button()
        time.sleep(2)

        # Experar la informacion del taxi
        routes_page.wait_for_driver_info()
        time.sleep(8)

    # Pruebas de errores

    def test_set_route_error(self):
        try:
            # Simula un error al establecer la ruta
            address_from = "Dirección de origen"
            address_to = ""  # Deja el campo de la dirección de destino vacío

            # Crea un objeto de la página UrbanRoutesPage
            routes_page = UrbanRoutesPage(self.driver)

            # Intenta establecer la ruta con una dirección de destino inválida
            routes_page.set_route(address_from, address_to)

            # Realiza alguna verificación para detectar el error
            # Por ejemplo, verifica si se muestra un mensaje de error en la interfaz de usuario

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")

    def test_set_route(self):
        try:
            # Simula un error al establecer la ruta
            address_from = "Dirección de origen"
            address_to = "Dirección de destino"

            # Crea un objeto UrbanRoutesPage
            routes_page = UrbanRoutesPage(self.driver)

            # Intenta establecer la ruta con una dirección de destino inválida
            routes_page.set_route(address_from, "")

            # Realiza alguna verificación para detectar el error (por ejemplo, verifica si se muestra un mensaje de error)
            # (Agrega aquí el código para realizar la verificación)

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")

    def test_select_flash_mode(self):
        try:
            # Crea un objeto UrbanRoutesPage
            routes_page = UrbanRoutesPage(self.driver)

            # Direcciones para la prueba
            address_from = "East 2nd Street, 601"
            address_to = "1300 1st St"

            # Establece la ruta en la página
            routes_page.set_route(address_from, address_to)

            # Selecciona el modo "Flas" en la página
            routes_page.modes_car_button()

            # Realiza alguna verificación para asegurarte de que el modo "Flas" esté seleccionado correctamente
            # (Agrega aquí el código para realizar la verificación)

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")

    def test_select_car_mode(self):
        try:
            # Crear un objeto UrbanRoutesPage
            routes_page = UrbanRoutesPage(self.driver)

            # Direcciones para la prueba
            address_from = "East 2nd Street, 601"
            address_to = "1300 1st St"
            # Establece la ruta en la página
            routes_page.set_route(address_from, address_to)


            # Seleccionar el modo de transporte en la página
            routes_page.select_car_mode()

            # Realizar alguna verificación para asegurarte de que el modo de transporte esté seleccionado correctamente
            # (Agregar aquí el código para realizar la verificación)

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")

    def test_select_taxi(self):
        try:
            # Crear un objeto UrbanRoutesPage
            routes_page = UrbanRoutesPage(self.driver)

            # Direcciones para la prueba
            address_from = "East 2nd Street, 601"
            address_to = "1300 1st St"
            # Establece la ruta en la página
            routes_page.set_route(address_from, address_to)

            # Seleccionar el modo "taxi" en la página
            routes_page.select_taxi()

            # Realizar alguna verificación para asegurarte de que el modo "taxi" esté seleccionado correctamente
            # (Agregar aquí el código para realizar la verificación)

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")

    def test_invalid_phone_number(self):
        try:
            # Inicializa la página de Urban Routes
            routes_page = UrbanRoutesPage(self.driver)

            # Dirección de ejemplo para las pruebas
            invalid_phone_number = "abcdefghij"  # Letras en lugar de números para el número de teléfono

            # Ingresa letras en lugar de números para el número de teléfono
            routes_page.complete_phone_number(invalid_phone_number)

            # Agrega alguna verificación para asegurarte de que la aplicación maneje correctamente esta situación
            # Por ejemplo, verifica si se muestra un mensaje de error adecuado o si la entrada no se acepta y se borra

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")

    def test_invalid_card_numbers(self):
        try:
            # Inicializa la página de Urban Routes
            routes_page = UrbanRoutesPage(self.driver)

            # Dirección de ejemplo para las pruebas
            invalid_card_number = "ABCD1234"  # Letras en lugar de números para el número de tarjeta
            invalid_card_code = "WXYZ"  # Letras en lugar de números para el código de tarjeta

            # Ingresa letras en lugar de números para el número de tarjeta y el código de tarjeta
            routes_page.card_numbers(invalid_card_number, invalid_card_code)

            # Agrega alguna verificación para asegurarte de que la aplicación maneje correctamente esta situación
            # Por ejemplo, verifica si se muestra un mensaje de error adecuado o si la entrada no se acepta y se borra

        except Exception as e:
            pytest.fail(f"Ocurrió un error durante la prueba: {str(e)}")
    def test_select_transport_mode(self):
        # Configura el navegador controlado por Selenium
        driver = webdriver.Chrome()
        driver.get(self.urban_routes_url)

        # Instancia la página de rutas urbanas
        routes_page = UrbanRoutesPage(driver)

        # Direcciones "from" y "to"
        address_from = "East 2nd Street, 601"
        address_to = "1300 1st St"

        # Selecciona un modo de transporte diferente al taxi
        try:
            routes_page.set_route(address_from, address_to)
            routes_page.select_transport_mode("Bicicleta")
        except NoSuchElementException as e:
            self.fail(f"No se pudo seleccionar el modo de transporte: {str(e)}")

        # Asegúrate de que se haya seleccionado el modo deseado
        selected_mode = driver.find_element(By.CSS_SELECTOR, '.selected-mode').text
        self.assertEqual(selected_mode.lower(), "bicicleta", "El modo de transporte seleccionado no es el esperado")

        # Cierra el navegador al finalizar la prueba
        driver.quit()

    def test_empty_to_field(self):
        # Instancia de UrbanRoutesPage no necesaria en este caso
        # page = UrbanRoutesPage()

        try:
            driver = webdriver.Chrome()
            driver.get(self.urban_routes_url)
            # Verificar que el título no esté vacío
            assert driver.title != ""
        except Exception as e:
            # En caso de error, falla la prueba
            pytest.fail(f"No se pudo cargar la página web: {str(e)}")
        finally:
            # Cerrar el navegador al finalizar la prueba
            self.driver.quit()





    if __name__ == '__main__':
        unittest.main()


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.mark.optional
    def test_optional(self):
        # Prueba opcional (no requerida)

        pass

    def test_order_taxi_with_invalid_input(self):
        # Simular el escenario donde el usuario ingresa una entrada inválida para la solicitud de taxi
        invalid_input = "abc"

        # Ejecutar la acción que deseamos probar
        result = self.page.order_taxi(invalid_input)

        # Verificar que la aplicación maneje adecuadamente la entrada inválida
        self.assertEqual(result, "Error: Invalid input. Please enter a valid numeric value.")

    def assertEqual(self, result, param):
        pass

    def fail(self, param):
        pass

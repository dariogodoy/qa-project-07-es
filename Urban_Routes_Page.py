import time

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import data


# Define the UrbanRoutesPage class with the necessary locators and methods
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    personal_button = (By.CSS_SELECTOR, '.modes-container .mode.active')
    mode_button = (By.CSS_SELECTOR, 'div.types-container div.type.active')
    taxi_button = (By.CLASS_NAME, 'button.round')
    comfort_field = (By.XPATH, '/html/body/div/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    button_phone_add = (By.CSS_SELECTOR, 'np-button')
    set_phone = (By.XPATH, '//*[@id="phone"]')
    button_next_add = (By.CSS_SELECTOR, 'div.buttons > button.button.full[type="submit"]')
    card_code_field = (By.ID, 'code')
    button_submit = (By.XPATH, '#root > div > div.number-picker.open > div.modal > '
                               'div.section.active > form > div.buttons > '
                               'button:nth-child(1)')
    paymeth_button = (By.CSS_SELECTOR, 'div.pp-button.filled')
    add_card_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    card_number_field = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]/input')
    cards_code_field = (By.CSS_SELECTOR, '.card-code-input > input:nth-child(1)')
    add_button = (By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    close_window = (By.CSS_SELECTOR, '.payment-picker > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)')
    message_field = (By.ID, 'comment')
    open_section = (By.CSS_SELECTOR, 'div.reqs-header')
    blanket_handkerchiefs_button = (By.CSS_SELECTOR, 'div.r-type-switch:nth-child(1) > div:nth-child(1) > '
                                                     'div:nth-child(2) > div:nth-child(1) > span:nth-child(2)')
    ice_cream_button = (By.CSS_SELECTOR, 'div.counter-plus')
    request_button = (By.CLASS_NAME, 'smart-butto')
    driver_info_modal = (By.CLASS_NAME, 'driver-info')

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, *locator):
        return self.driver.find_element(*locator)

    def set_route(self, address_from: str, address_to: str):
        """Sets the route from the 'from' field to the 'to' field.

        Args:
            address_from (str): The address to enter in the 'from' field.
            address_to (str): The address to enter in the 'to' field.
        """
        self.driver.get(data.urban_routes_url)

        # Wait for the page to be loaded
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located((By.ID, "root")))

        # Espera hasta que el elemento "from" esté presente y visible
        from_field = wait.until(EC.visibility_of_element_located((By.ID, "from")))
        from_field.send_keys(address_from)
        from_field.send_keys(Keys.RETURN)

        # Espera hasta que el elemento "from" esté presente y visible
        to_field = wait.until(EC.visibility_of_element_located((By.ID, "to")))
        to_field.send_keys(address_to)
        to_field.send_keys(Keys.RETURN)
        time.sleep(2)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def modes_car_button(self):
        # Esperar hasta que el botón del modo "Personal" esté presente y sea visible
        personal_button = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, '.modes-container .mode:nth-child(3)'))
        )

        # Verificar si el modo "Personal" ya está activo
        if 'active' not in personal_button.get_attribute('class'):
            # Hacer clic en el botón del modo "Personal"
            personal_button.click()

    def select_car_mode(self):
        # Encontrar y hacer clic en el botón del carro
        car_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.types-container div.type.active'))
        )
        car_button.click()

    def select_taxi(self):
        # Espera hasta que el botón de taxi esté visible y haga clic en él
        WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'button.round'))
        ).click()

    def select_comfort_rate(self):
        WebDriverWait(self.driver, 30).until(EC.title_contains("Urban"))

        # Encuentra el botón asociado a la tarifa "Comfort"
        comfort_tariff_button = self.driver.find_element(By.XPATH,
                                                         '/html/body/div/div/div[3]/div[3]/div[2]/div[1]/div[5]')
        # Haz clic en el botón de la tarifa "Comfort"
        comfort_tariff_button.click()

    def get_comfort_tariff(self):
        comfort_text = self.driver.find_element(*self.comfort_field).text
        return comfort_text.split('\n')[0]  # Obtener solo la parte antes del salto de línea y el precio

    def add_phone_button(self):
        # Esperar a que el botón de teléfono esté presente y sea interactivo
        wait = WebDriverWait(self.driver, 20)
        phone_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'np-button')))

        # Hacer clic en el botón de teléfono
        phone_button.click()

    def complete_phone_number(self, phone_number):
        # Esperar a que el campo de número de teléfono esté presente y sea interactivo
        wait = WebDriverWait(self.driver, 40)
        phone_input = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="phone"]')))

        # Limpiar el campo de entrada antes de ingresar el número de teléfono
        phone_input.clear()

        # Ingresar el número de teléfono en el campo de entrada
        phone_input.send_keys(phone_number)

    def get_set_phone(self):
        phone_element = self.driver.find_element(*self.set_phone)
        return phone_element.get_attribute('value') if phone_element is not None else None

    def click_next_button(self):
        # Esperar a que el botón "Siguiente" esté presente y sea interactivo
        wait = WebDriverWait(self.driver, 30)
        next_button = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.buttons > button.button.full[type="submit"]')))

        # Hacer clic en el botón "Siguiente"
        next_button.click()

    def confirm_button_click(self):
        # Esperar a que el botón de confirmación esté presente y sea interactivo
        confirm_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#root > div > div.number-picker.open > div.modal > '
                                                         'div.section.active > form > div.buttons > '
                                                         'button:nth-child(1)'))
        )

        # Verificar si el botón de confirmación está habilitado para hacer clic
        if confirm_button.is_enabled():
            confirm_button.click()

    def pay_method_click(self):

        # Intentar hacer clic en el botón de método de pago usando JavaScript
        try:
            # Encontrar el elemento del botón de método de pago
            payment_method_button = WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.pp-button.filled'))
            )

            # Hacer clic en el botón de método de pago usando JavaScript
            self.driver.execute_script("arguments[0].click();", payment_method_button)

            print("Se ha seleccionado el método de pago correctamente.")
        except Exception as e:
            print("Error al seleccionar el método de pago:", e)

    def add_card(self):
        # Localizador del botón "Agregar tarjeta"
        add_card_button_locator = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')

        # Esperar a que el botón "Agregar tarjeta" esté presente y sea interactivo
        wait = WebDriverWait(self.driver, 60)
        add_card_button = wait.until(EC.element_to_be_clickable(add_card_button_locator))

        # Hacer clic en el botón "Agregar tarjeta"
        add_card_button.click()

    def card_numbers(self, card_number: str, card_code: str):
        """Enters the card number and code.

        Args:
            card_number (str): The card number to enter.
            card_code (str): The card code to enter.
        """
        # Encuentra el campo de entrada para el número de tarjeta y lo completa
        card_number_field = self.driver.find_element(By.XPATH,
                                                     '/html/body/div/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div['
                                                     '2]/input')
        card_number_field.send_keys(card_number)

        # Encuentra el campo de entrada para el código de la tarjeta y lo completa
        card_code_field = self.driver.find_element(By.CSS_SELECTOR, '.card-code-input > input:nth-child(1)')

        card_code_field.send_keys(card_code)

        # Simula presionar la tecla TAB para activar el siguiente campo (si es necesario)
        card_code_field.send_keys(Keys.TAB)

    def get_card_number(self):
        return self.driver.find_element(*self.card_number_field).get_property('value')

    def get_card_code(self):
        card_code_field = self.driver.find_element(*self.card_code_field)
        return card_code_field.get_attribute('value')

    def click_add_button(self):
        """Clicks the 'Add' button."""
        # Espera hasta que el botón de "Agregar" esté presente y sea interactivo
        add_button = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div[2]/div[2]/form/div[3]/button[1]'))
        )

        # Hace clic en el botón de "Agregar"
        add_button.click()

    def close_popup_window(self):
        # Espera hasta que el botón de cierre de la ventana emergente esté presente y sea clickeable
        close_button = WebDriverWait(self.driver, 40).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.payment-picker > div:nth-child(2) > div:nth-child(1) > button:nth-child(1)'))
        )
        # Haz clic en el botón de cierre de la ventana emergente
        close_button.click()

    def test_set_message_for_driver(self):
        # Aumentar el tiempo de espera
        wait = WebDriverWait(self.driver, 40)

        # Esperar hasta que aparezca el campo de entrada para el mensaje
        comment_input = wait.until(EC.visibility_of_element_located((By.ID, 'comment')))

        # Ingresar un mensaje para el conductor
        message = "Hola, buenas noches."
        comment_input.send_keys(message)

    def get_message(self):
        message_fiel = self.driver.find_element(*self.message_field)
        return message_fiel.get_attribute('value')

    def click_blanket_handkerchiefs(self):
        # Encuentra el interruptor para solicitar la manta y los pañuelos y haz clic en él
        blanket_tissues_switch = self.driver.find_element(By.CSS_SELECTOR, 'div.r-type-switch:nth-child(1) > '
                                                                           'div:nth-child(1) > div:nth-child(2) > '
                                                                           'div:nth-child(1) > span:nth-child(2)')
        blanket_tissues_switch.click()

    def get_blanket_handkerchiefs(self):
        blanket_tissues_switch = self.driver.find_element(By.CSS_SELECTOR, '.switch input[type="checkbox"]')
        return blanket_tissues_switch.is_selected()

    def increment_ice_cream(self):
        plus_button = self.driver.find_element(By.CSS_SELECTOR, 'div.counter-plus')
        plus_button.click()

    def get_ice_button(self):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.counter-plus'))
            )
            return element
        except:
            return False

    def click_call_taxi_button(self):
        # Espera hasta que el botón "Call a taxi" sea clickeable
        call_taxi_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'smart-button'))
        )
        call_taxi_button.click()

    def get_call_taxi_button(self):
        # Waits up to 10 seconds for the "Call a taxi" button to be present
        call_taxi_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button.smart-button'))
        )
        return call_taxi_button

    def wait_for_driver_info(self):
        # Espera hasta que la información del conductor esté presente en el modal
        WebDriverWait(self.driver, 40).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'driver-info'))
        )

    def add_credit_card(self, card_number, card_code):
        pass

    def get_selected_mode(self):
        pass

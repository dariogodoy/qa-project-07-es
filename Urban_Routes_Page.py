from selenium.common import TimeoutException, NoSuchElementException
import data
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from Phone_py.code_phone_retrive import retrieve_phone_code



# Define the UrbanRoutesPage class with the necessary locators and methods
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    personal_button = (By.CSS_SELECTOR, '.modes-container .mode.active')
    mode_button = (By.CSS_SELECTOR, 'div.types-container div.type.active')
    taxi_button = (By.CLASS_NAME, 'button.round')
    comfort_field = (By.CSS_SELECTOR, 'html body div#root div.app div.workflow div.workflow-subcontainer '
                                      'div.tariff-picker.shown div.tariff-cards div.tcard.active '
                                      'button.i-button.tcard-i.active')
    button_phone_add = (By.CSS_SELECTOR, 'np-button')
    set_phone = (By.CSS_SELECTOR, ' .np-input')
    button_next_add = (By.CSS_SELECTOR, 'div.buttons > button.button.full[type="submit"]')
    add_card_button = (By.ID, 'add-card_button')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')
    message_field = (By.ID, 'comment')
    request_button = (By.ID, "request_button")
    driver_info_modal = (By.ID, "driver_info_modal")
    blanket_tissues_button = (By.ID, "blanket-tissues_button")
    ice_cream_button = (By.ID, "ice-cream_button")

    def __init__(self, driver):
        self.driver = driver


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
        try:
            # Esperar hasta que el botón del modo "Personal" esté presente y sea visible
            personal_button = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, '.modes-container .mode:nth-child(3)'))
            )

            # Verificar si el modo "Personal" ya está activo
            if 'active' in personal_button.get_attribute('class'):
                print("El modo 'Personal' ya está seleccionado.")
            else:
                # Hacer clic en el botón del modo "Personal"
                personal_button.click()
                print("Se ha seleccionado el modo 'Personal'.")

        except TimeoutException:
            print("Tiempo de espera agotado. El botón del modo 'Personal' no está disponible.")
        except NoSuchElementException:
            print("No se encontró el modo 'Personal'.")
        except Exception as e:
            print("Error al seleccionar el modo 'Personal':", e)

    def select_car_mode(self):
        try:
            # Encontrar y hacer clic en el botón del carro
            car_button = self.driver.find_element(By.CSS_SELECTOR, 'div.types-container div.type.active')
            car_button.click()

            # Verificar si el botón del carro se ha seleccionado correctamente
            if 'active' in car_button.get_attribute('class'):
                print("Se ha seleccionado el modo 'Carro'.")
            else:
                print("No se pudo seleccionar el modo 'Carro'.")
        except NoSuchElementException:
            print("No se encontró el botón 'Carro'.")
        except Exception as e:
            print("Error al seleccionar el modo 'Carro':", e)

    def select_taxi(self):
        try:
            # Espera hasta que el botón de taxi esté visible y haga clic en él
            WebDriverWait(self.driver, 30).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'button.round'))
            ).click()
        except Exception as e:
            print("Error al hacer clic en el botón de taxi:", e)

    def select_comfort_rate(self):
        try:
            print("Esperando a que la página se cargue completamente...")
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.title_contains("Urban"))

            print("Buscando la tarjeta de tarifa Comfort...")
            # Seleccionar la quinta tarjeta de tarifa activa
            tariff_card = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'html body div#root div.app '
                                                                                        'div.workflow '
                                                                                        'div.workflow-subcontainer '
                                                                                        'div.tariff-picker.shown '
                                                                                        'div.tariff-cards '
                                                                                        'div.tcard.active')))

            # Hacer clic en la tarjeta de tarifa
            print("Haciendo clic en la tarjeta de tarifa Comfort...")
            tariff_card.click()
            print("Se ha seleccionado la tarjeta de tarifa Comfort.")

        except Exception as e:
            print("Error al seleccionar la tarjeta de tarifa Comfort:", e)

    def add_phone_button(self):
        global wait
        try:
            # Esperar a que el botón de teléfono esté presente y sea interactivo
            wait = WebDriverWait(self.driver, 20)
            phone_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'np-button')))

            # Hacer clic en el botón de teléfono
            phone_button.click()

            print('Botón de teléfono agregado correctamente.')

        except Exception as e:
            print("Error al agregar el botón de teléfono:", e)

    def complete_phone_number(self, phone_number):
        try:
            # Esperar a que el campo de número de teléfono esté presente y sea interactivo
            wait = WebDriverWait(self.driver, 40)
            phone_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.np-input input#phone')))

            # Limpiar el campo de entrada antes de ingresar el número de teléfono
            phone_input.clear()

            # Ingresar el número de teléfono en el campo de entrada
            phone_input.send_keys(phone_number)

            print('Número de teléfono ingresado correctamente.')

        except Exception as e:
            print("Error al ingresar el número de teléfono:", e)

    def click_next_button(self):
        try:
            # Esperar a que el botón "Siguiente" esté presente y sea interactivo
            wait = WebDriverWait(self.driver, 500)
            next_button = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.buttons > button.button.full[type="submit"]')))

            # Hacer clic en el botón "Siguiente"
            next_button.click()

            print('Se ha hecho clic en el botón "Siguiente" correctamente.')

            time.sleep(10)

        except Exception as e:
            print("Error al hacer clic en el botón 'Siguiente':", e)

    def code_phone(self):
        try:
            phone_code = retrieve_phone_code(self.driver)
            print("El código de confirmación del teléfono es:", phone_code)
            return phone_code  # Devuelve el código de confirmación

        except Exception as e:
            print("Ocurrió un error al intentar obtener el código de confirmación del teléfono:", e)
            return None  # Devuelve None si no se puede obtener el código de confirmación

    def check_code(self, phone_code=None):
        try:
            # Si no se proporciona un código de teléfono, obtén uno
            if phone_code is None:
                phone_code = self.code_phone()

            # Verifica que se haya obtenido un código válido
            if phone_code:
                # Busca el elemento de etiqueta asociado al campo de entrada de código
                label_element = self.driver.find_element(By.CSS_SELECTOR, 'label.label[for="code"]')

                # Ingresa el código en el campo de entrada correspondiente
                code_input = self.driver.find_element(By.ID, 'codigo_confirmacion')
                code_input.send_keys(phone_code)

                # Envía el formulario de verificación
                submit_button = self.driver.find_element(By.ID, 'submit_button')
                submit_button.click()

                print(
                    "El formulario de verificación se ha completado con éxito utilizando el código de confirmación del teléfono.")

        except Exception as e:
            print("Ocurrió un error al intentar ajustar el código de confirmación:", e)
    def card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def card_number(self, card_number, card_code):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        self.driver.find_element(*self.card_code_field).send_keys(card_code)
        # Simulate pressing TAB to activate the 'link' button
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB)
        # Click the 'link' button to add the credit card
        self.driver.find_element(By.LINK_TEXT, 'link').click()

    def test_set_message_for_driver(self):
        wait = WebDriverWait(self.driver, 20)  # Aumentar el tiempo de espera
        try:
            comment_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'comment')))
            # Realizar acciones con el elemento encontrado, si es necesario
        except TimeoutException:
            print("El elemento con la clase 'comment' no se encontró dentro del tiempo de espera")

    def request_ride(self):
        self.driver.find_element(*self.request_button).click()

    def click_blanket_tissues(self):
        self.driver.find_element(*self.blanket_tissues_button).click()

    def click_ice_cream(self):
        self.driver.find_element(*self.ice_cream_button).click()

    def wait_for_driver_info_modal(self):
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, "driver_info_modal")))

    def add_credit_card(self, card_number, card_code):
        pass

    def get_selected_mode(self):
        pass








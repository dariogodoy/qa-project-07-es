import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el "
                            "código en tu aplicación.")
        return code


# Define the UrbanRoutesPage class with the necessary locators and methods
class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    personal_button = (By.CLASS_NAME, 'modes-container')
    car_type_item = (By.CLASS_NAME, 'types-container')
    comfort_field = (By.ID, 'tariff-card-4')
    phone_field = (By.CLASS_NAME, 'np-text')
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
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "root")))

        from_field = self.driver.find_element(By.ID, "from")
        from_field.send_keys(address_from)
        from_field.send_keys(Keys.RETURN)

        to_field = self.driver.find_element(By.ID, "to")
        to_field.send_keys(address_to)
        to_field.send_keys(Keys.RETURN)
        time.sleep(2)

    def set_from(self, from_address):
        driver = self.driver
        login_input = driver.find_element(*self.from_field)
        login_input.send_keys(from_address)

    def set_to(self, to_address):
        driver = self.driver
        login_input = driver.find_element(*self.to_field)
        login_input.send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def modes_button(self):
        self.driver.find_element(*self.personal_button).click()

    def select_comfort_rate(self):
        """Selects the Comfort rate."""
        # Wait for the page to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.title_contains("Urban Routes"))

        # Click on the Comfort rate
        comfort_rate = wait.until(EC.element_to_be_clickable((By.ID, "rate-comfort")))
        comfort_rate.click()

    def set_phone(self, phone_number):
        driver = self.driver
        phone_input = driver.find_element(*self.phone_field)
        phone_input.send_keys(phone_number)

    def card_button(self):
        self.driver.find_element(*self.add_card_button).click()

    def card_number(self, card_number, card_code):
        self.driver.find_element(*self.card_number_field).send_keys(card_number)
        self.driver.find_element(*self.card_code_field).send_keys(card_code)
        # Simulate pressing TAB to activate the 'link' button
        self.driver.find_element(*self.card_code_field).send_keys(Keys.TAB)
        # Click the 'link' button to add the credit card
        self.driver.find_element(By.LINK_TEXT, 'link').click()

    def set_message(self, message):
        driver = self.driver
        message_input = driver.find_element(*self.message_field)
        message_input.send_keys(message)

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


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado
        # para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = 'data.address_from'
        address_to = 'data.address_to'
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_request_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)

        # Set the route
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

        # Wait for the Comfort rate to be clickable
        wait = WebDriverWait(self.driver, 10)
        comfort_rate = wait.until(EC.element_to_be_clickable((By.ID, "rate-comfort")))
        comfort_rate.click()

    def test_modes_taxi(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.modes_button()

    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort_rate()

    def test_set_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_phone(data.phone_number)

    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_credit_card(data.card_number, data.card_code)

    def test_set_message_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_message(data.message_for_driver)

        # Select the Comfort rate
        routes_page.select_comfort_rate()

        # Set the phone number
        phone_number = data.phone_number
        routes_page.set_phone(phone_number)

        # Add a credit card
        card_number = data.card_number
        card_code = data.card_code
        routes_page.add_credit_card(card_number, card_code)

        # Set the message for the driver
        message = data.message_for_driver
        routes_page.set_message(message)

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

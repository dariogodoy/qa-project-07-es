from selenium import webdriver
import pytest
from Urban_Routes_Page import UrbanRoutesPage
import data
import time


class TestUrbanRoutes:
    driver = None
    urban_routes_url = 'https://cnt-b00e8320-e66b-4a81-9f42-12d05ba4cfd5.containerhub.tripleten-services.com'

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado
        # para recuperar el código de confirmación del teléfono
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

        #Completar el numero de telefono
        phone_number = '+1 123 123 12 12'
        routes_page.complete_phone_number(phone_number)

        #Dar click en siguiente
        routes_page.click_next_button()
        time.sleep(10)

        #Codigo de configuracion
        routes_page.code_phone()

        #Codigo del telefono
        # Código de configuración
        phone_code = '8656'  # Supongamos que tienes el código de confirmación del teléfono
        routes_page.check_code(phone_code)

    def test_modes_car_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.modes_car_button()

    def test_select_car_mode(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_car_mode()

    def test_select_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_taxi()


    def test_select_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.select_comfort_rate()

    def test_add_phone_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_phone_button()

    def test_complete_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.complete_phone_number(data.phone_number)


    def test_add_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.add_credit_card(data.card_number, data.card_code)


    def test_click_next_button(self):
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_next_button()





    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

    @pytest.mark.optional
    def test_optional(self):
        # Prueba opcional (no requerida)
        pass
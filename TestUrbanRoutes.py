from Urban_Routes_Page import UrbanRoutesPage
import time
import data
from selenium import webdriver
from code_phone_retrive import retrieve_phone_code, enter_confirmation_code


class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de
        # confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_comfort_tariff(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()

        # Seleccionar la tarifa de confort
        routes_page.select_comfort_rate()

        # Verificar que la tarifa seleccionada sea la tarifa de confort
        assert routes_page.get_comfort_tariff() == "Comfort"

    def test_phone_number(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()
        routes_page.select_comfort_rate()
        routes_page.add_phone_button()

        # Otros pasos que puedan ser necesarios antes de ingresar el número de teléfono, por ejemplo, seleccionar una
        # tarifa

        # Ingresar el número de teléfono
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)

        assert routes_page.get_set_phone() == phone_number

    def test_credit_card(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()
        routes_page.select_comfort_rate()
        routes_page.add_phone_button()
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)
        routes_page.click_next_button()
        code = retrieve_phone_code(self.driver)
        print("Phone code: " + code)
        enter_confirmation_code(self.driver, code)
        routes_page.confirm_button_click()
        routes_page.pay_method_click()
        routes_page.add_card()
        time.sleep(2)

        # Ingresa los datos de la tarjeta
        card_number = data.card_number
        card_code = data.card_code
        routes_page.card_numbers(card_number, card_code)
        assert routes_page.get_card_number() == card_number

    def test_message_to_driver(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()
        routes_page.select_comfort_rate()
        routes_page.add_phone_button()
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)
        routes_page.click_next_button()
        code = retrieve_phone_code(self.driver)
        print("Phone code: " + code)
        enter_confirmation_code(self.driver, code)
        routes_page.confirm_button_click()
        routes_page.pay_method_click()
        routes_page.add_card()
        time.sleep(2)
        card_number = data.card_number
        card_code = data.card_code
        routes_page.card_numbers(card_number, card_code)
        routes_page.click_add_button()
        routes_page.close_popup_window()

        # Dejar un comentario
        routes_page.test_set_message_for_driver()
        time.sleep(3)
        assert routes_page.get_message()

    def test_request_drive(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()
        routes_page.select_comfort_rate()
        routes_page.add_phone_button()
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)
        routes_page.click_next_button()
        code = retrieve_phone_code(self.driver)
        print("Phone code: " + code)
        enter_confirmation_code(self.driver, code)
        routes_page.confirm_button_click()
        routes_page.pay_method_click()
        routes_page.add_card()
        time.sleep(2)
        card_number = data.card_number
        card_code = data.card_code
        routes_page.card_numbers(card_number, card_code)
        routes_page.click_add_button()
        routes_page.close_popup_window()
        routes_page.test_set_message_for_driver()
        time.sleep(3)

        # Elegir manta
        routes_page.click_blanket_handkerchiefs()
        assert routes_page.get_blanket_handkerchiefs()
        time.sleep(2)

    def test_ice_cream(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()
        routes_page.select_comfort_rate()
        routes_page.add_phone_button()
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)
        routes_page.click_next_button()
        code = retrieve_phone_code(self.driver)
        print("Phone code: " + code)
        enter_confirmation_code(self.driver, code)
        routes_page.confirm_button_click()
        routes_page.pay_method_click()
        routes_page.add_card()
        time.sleep(2)
        card_number = data.card_number
        card_code = data.card_code
        routes_page.card_numbers(card_number, card_code)
        routes_page.click_add_button()
        routes_page.close_popup_window()
        routes_page.test_set_message_for_driver()
        time.sleep(3)
        routes_page.click_blanket_handkerchiefs()
        time.sleep(2)

        # Elegir helados
        routes_page.increment_ice_cream()
        routes_page.increment_ice_cream()
        time.sleep(3)
        assert routes_page.get_ice_button()

    def test_search_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.modes_car_button()
        routes_page.select_car_mode()
        routes_page.select_taxi()
        routes_page.select_comfort_rate()
        routes_page.add_phone_button()
        phone_number = '+11231231212'
        routes_page.complete_phone_number(phone_number)
        routes_page.click_next_button()
        code = retrieve_phone_code(self.driver)
        print("Phone code: " + code)
        enter_confirmation_code(self.driver, code)
        routes_page.confirm_button_click()
        routes_page.pay_method_click()
        routes_page.add_card()
        time.sleep(2)
        card_number = data.card_number
        card_code = data.card_code
        routes_page.card_numbers(card_number, card_code)
        routes_page.click_add_button()
        routes_page.close_popup_window()
        routes_page.test_set_message_for_driver()
        time.sleep(3)
        routes_page.click_blanket_handkerchiefs()
        time.sleep(2)
        routes_page.increment_ice_cream()
        routes_page.increment_ice_cream()
        time.sleep(3)
        routes_page.increment_ice_cream()
        routes_page.increment_ice_cream()
        time.sleep(3)

        # Dar click en llamar taxi
        routes_page.click_call_taxi_button()
        time.sleep(2)
        assert routes_page.get_call_taxi_button()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

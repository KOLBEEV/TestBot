from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import tempfile
from selenium.webdriver.chrome.options import Options
import time


class SurveyBot:
    def __init__(self, survey_url, id=1):
        self.survey_url = survey_url
        self.id = id

        temp_dir = tempfile.mkdtemp()

        options = Options()
        options.add_argument(f"--user-data-dir={temp_dir}")  # Временный каталог
        options.add_argument("--start-maximized")
        options.add_argument("--disable-infobars")
        options.add_argument("--no-sandbox")  # Для Linux систем

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def start_survey(self):
        self.driver.get(self.survey_url)

        self.click_next()

        self.start_test()

        self.driver.quit()


    def start_test(self):
        #1
        zero_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'gradientNumber') and text()='0']"))
        )
        zero_element.click()
        self.click_next()

        #2
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Очень плохое')]"))
        )
        element.click()
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//p[contains(text(), 'Да')]"))
        )
        element.click()
        self.click_next()

        #3
        self.choose_checkbox_grid(check_box_number=4)

        #4
        self.choose_checkbox_grid(check_box_number=6)

        #5
        self.choose_checkbox_grid(check_box_number=5)

        #6
        self.choose_checkbox_grid(check_box_number=3)

        #7
        self.choose_checkbox_grid(check_box_number=3)

        #8
        self.choose_checkbox_grid(check_box_number=4)

        #9
        self.click_next()

        #10
        element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Все жители России')]"))
        )
        element.click()
        self.choose_checkbox_grid(check_box_number=1)

        #11
        self.choose_checkbox_grid(check_box_number=5)

        #12
        input_fields = self.driver.find_elements(By.XPATH,
                                                 "//div[contains(@class, 'groupFreeAnswers')]//input[@type='string']")

        # Заполняем поля целями
        for field in input_fields:
            field.clear()
            field.send_keys('Отчислиться')
            time.sleep(0.015)  # Пауза между вводом

        self.choose_checkbox_grid(check_box_number=5)

        #13
        self.choose_checkbox_grid(check_box_number=5)

        #14
        self.click_checkbox_by_question_text(
            question_text='Кто-то из членов Вашей семьи участвует/участвовал в СВО?',
            option_text='Нет'
        )
        self.click_checkbox_by_question_text(
            question_text='Отметьте, что из перечисленного к Вам относится:',
            option_text='Ничего из перечисленного'
        )
        self.click_checkbox_by_question_text(
            question_text='Вы участвовали в СВО?',
            option_text='Нет'
        )
        self.click_checkbox_by_question_text(
            question_text='С какими сложными жизненными ситуациями Вам пришлось столкнуться ',
            option_text='Ничего из перечисленного'
        )
        self.click_next()

        #15
        self.choose_checkbox_grid(check_box_number=5)

        #16
        self.fill_field(title="Ваш возраст:", text="20")
        self.click_checkbox_by_question_text(
            question_text="Пол:",
            option_text="Мужской"
        )
        self.fill_field(title="На каком курсе Вы сейчас учитесь?", text="3")
        self.click_checkbox_by_question_text(
            question_text="Направление подготовки:",
            option_text="Бакалавриат"
        )
        self.click_checkbox_by_question_text(
            question_text="Где Вы проживаете в настоящее время?",
            option_text="Общежитие"
        )
        self.click_checkbox_by_question_text(
            question_text="Образование:",
            option_text="Высшее"
        )
        self.click_checkbox_by_question_text(
            question_text="Ваша занятость в настоящее время:",
            option_text="Студент"
        )
        self.click_checkbox_by_question_text(
            question_text="Выберите то, что к Вам относится:",
            option_text="Холост"
        )
        self.click_checkbox_by_question_text(
            question_text="Есть ли у Вас ребёнок/дети?",
            option_text="Да"
        )
        self.click_checkbox_by_question_text(
            question_text="Оцените, пожалуйста, Ваше материальное положение:",
            option_text="Плохое"
        )
        self.click_checkbox_by_question_text(
            question_text="Изменилось ли Ваше материальное положение за последние три года?",
            option_text="Ухудшилось"
        )
        self.click_next(text="Отправить")


    def fill_field(self, title, text):
        try:
            # Экранируем кавычки в title и добавляем в XPath
            xpath = f'//div[contains(., "{title}")]/following-sibling::div//input'

            # Ждём пока поле станет доступным
            input_field = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )

            # Прокручиваем и вводим текст
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", input_field)
            time.sleep(0.03)

            # Очищаем и вводим текст (3 варианта на выбор)
            try:
                # Способ 1: Обычный ввод
                input_field.clear()
                input_field.send_keys(text)
            except:
                # Способ 2: JavaScript ввод
                self.driver.execute_script(f"arguments[0].value = '{text}';", input_field)
                # Способ 3: Для React/angular приложений
                self.driver.execute_script(
                    "var nativeInputValueSetter = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype, 'value').set;" +
                    "nativeInputValueSetter.call(arguments[0], arguments[1]);" +
                    "var event = new Event('input', { bubbles: true });" +
                    "arguments[0].dispatchEvent(event);",
                    input_field, text)

            time.sleep(0.05)
            return True

        except Exception as e:
            print(f"Не удалось заполнить поле '{title}': {str(e)}")
            self._take_screenshot(f"error_{title}")
            return False


    def click_checkbox_by_question_text(self, question_text, option_text):
        """Клик по варианту в определенном вопросе"""
        question = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            f"//div[contains(@class, 'header__') and contains(., '{question_text}')]/ancestor::div[contains(@class, 'question__')]"))
        )
        label = question.find_element(By.XPATH, f".//div[contains(@class, 'label__') and contains(., '{option_text}')]")
        checkbox = label.find_element(By.XPATH, "./preceding-sibling::div[contains(@class, 'control__')]")
        self.driver.execute_script("arguments[0].click();", checkbox)


    def choose_checkbox_grid(self, check_box_number):
        # Находим все строки с вопросами (каждая строка содержит 4 чекбокса)
        question_rows = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'answer row__')]"))
        )

        for row in question_rows:
            try:
                # Находим все чекбоксы в текущей строке
                checkboxes = row.find_elements(By.XPATH, ".//div[contains(@class, 'checkbox__')]")

                checkbox = checkboxes[check_box_number-1]
                self.driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
                time.sleep(0.01)
                self.driver.execute_script("arguments[0].click();", checkbox)
                time.sleep(0.015)
            except Exception as e:
                print(f"Ошибка при обработке строки: {str(e)}")
                continue

        # После ответа на все вопросы нажимаем "Далее"
        self.click_next()


    def click_next(self, text="Далее"):
        next_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//button[.//span[contains(text(), '{text}')]]"))
        )
        next_button.click()

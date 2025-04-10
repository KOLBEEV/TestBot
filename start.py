from survey_bot import SurveyBot
from config import URL, WINDOWS_COUNT, ITERATIONS
import threading
import time


def run_bot(id):
    bot = SurveyBot(URL, id)
    for i in range(ITERATIONS):
        bot.start_survey()
        time.sleep(2)


if __name__ == "__main__":
    threads = []

    for i in range(WINDOWS_COUNT):
        thread = threading.Thread(target=run_bot, args=(i+1,))
        threads.append(thread)
        thread.start()
        time.sleep(1)

    for thread in threads:
        thread.join()

    print("END!")

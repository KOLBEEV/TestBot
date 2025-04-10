from survey_bot import SurveyBot
from config import URL, WINDOWS_COUNT, ITERATIONS
import threading
import time


def run_bot(id):
    bot = SurveyBot(URL, id)
    bot.start_survey()
    time.sleep(0.1)


if __name__ == "__main__":
    threads = []
    for j in range(ITERATIONS):
        for i in range(WINDOWS_COUNT):
            thread = threading.Thread(target=run_bot, args=(i+1,))
            threads.append(thread)
            thread.start()
            time.sleep(0.1)

        for thread in threads:
            thread.join()

    print("END!")

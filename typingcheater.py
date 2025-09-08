import time
from selenium import webdriver
from selenium.common.exceptions import InvalidSessionIdException, NoSuchWindowException
from selenium.webdriver.common.by import By

# Launch browser
def startDemo():
    driver = webdriver.Chrome()
    driver.get("https://monkeytype.com/")

    time.sleep(3)  # wait for page to load

    # Focus typing area
    driver.find_element(By.TAG_NAME, "body").click()

    while True:
        try:
            # Get the currently active word
            active_word = driver.find_element(By.CSS_SELECTOR, "#words .word.active")
            letters = active_word.find_elements(By.TAG_NAME, "letter")

            # Build word text from letters
            word_text = "".join([letter.text for letter in letters])

            # Type word + space
            driver.switch_to.active_element.send_keys(word_text + " ")

            # Small delay so Monkeytype updates active word
            time.sleep(0.05)
        except KeyboardInterrupt:
            break
        except InvalidSessionIdException:
            break
        except NoSuchWindowException:
            break
        except ConnectionResetError:
            break
        except Exception as e:
            print("Stop")
            print(e)

    try:
        driver.quit()
    except Exception:
        return

if __name__ == '__main__':
    startDemo()

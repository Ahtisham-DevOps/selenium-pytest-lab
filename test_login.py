import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://www.saucedemo.com/"

# (username, password, expected)
CASES = [
    pytest.param("standard_user", "secret_sauce", "inventory", id="valid"),
    pytest.param("locked_out_user", "secret_sauce", "locked out", id="locked"),
    pytest.param("standard_user", "wrong_pass", "do not match", id="wrong_password"),
]


@pytest.mark.smoke
@pytest.mark.parametrize("username,password,expected", CASES)
def test_login(driver, username, password, expected):
    wait = WebDriverWait(driver, 10)
    driver.get(URL)

    wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()

    if expected == "inventory":
        wait.until(EC.url_contains("inventory"))
        assert "inventory" in driver.current_url, "Login ke baad inventory page nahi khula"
    else:
        err = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        ).text
        assert expected in err, f"Error text mein '{expected}' nahi mila, mila: {err}"

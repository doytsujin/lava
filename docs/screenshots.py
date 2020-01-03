import argparse
from getpass import getpass
import pathlib
import sys
import yaml

import selenium
from selenium import webdriver


class LAVA:
    LOGIN_PAGE = "/accounts/login/"
    LOGOUT_PAGE = "/accounts/logout/"

    MENUS = {
        "scheduler": "glyphicon-calendar",
    }
    WIDTH = 1280
    HEIGHT = 960

    def __init__(self, options):
        self.options = options
        self.driver = selenium.webdriver.Chrome()
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(LAVA.WIDTH, LAVA.HEIGHT)

    def __del__(self):
        self.driver.quit()

    def find(self, selector):
        return self.driver.find_element_by_css_selector(selector)

    def login(self):
        self.driver.get(self.options.url + LAVA.LOGIN_PAGE)
        self.driver.find_element_by_id("id_username").send_keys(self.options.username)
        self.driver.find_element_by_id("id_password").send_keys(self.options.password)
        self.driver.find_element_by_css_selector("button.btn-success").click()

    def logout(self):
        self.driver.get(self.options.url + LAVA.LOGOUT_PAGE)

    def menu(self, name):
        return self.driver.find_element_by_css_selector(
            "a.dropdown-toggle > span.%s" % LAVA.MENUS[name]
        )

    def add_border(self, selector):
        self.driver.execute_script(
            "document.querySelector(\"%s\").style['border'] = 'solid'" % selector
        )
        self.driver.execute_script(
            "document.querySelector(\"%s\").style['border-color'] = 'red'" % selector
        )

    def screenshot(self, filename):
        # TODO: save into the right sub-directory
        self.driver.get_screenshot_as_file(filename)

    def __call__(self, name, actions):
        for action in actions:
            # Check that action is a dict with only one key (the action name)
            assert isinstance(action, dict)
            assert len(action.keys()) == 1
            action_name = list(action.keys())[0]
            self._handle(action_name, action[action_name])
        self.screenshot(name + ".png")

    def _handle(self, action, params):
        name = "_handle_" + action.replace(".", "_")
        if not hasattr(self, name):
            raise NotImplementedError("Unknow action %r" % action)
        return getattr(self, name)(params)

    def _handle_click(self, params):
        assert isinstance(params, str)
        self.find(params).click()

    def _handle_get(self, params):
        assert isinstance(params, str)
        self.driver.get(self.options.url + params)

    def _handle_highlight(self, params):
        assert isinstance(params, str)
        self.add_border(params)

    def _handle_login(self, params):
        assert params is None
        self.login()

    def _handle_logout(self, params):
        assert params is None
        self.logout()

    def _handle_menu_click(self, params):
        assert isinstance(params, str)
        assert params in LAVA.MENUS
        self.menu(params).click()

    def _handle_send_keys(self, params):
        assert isinstance(params, dict)
        assert set(params.keys()) == set(["selector", "content"])
        self.find(params["selector"]).send_keys(params["content"])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", required=True)
    parser.add_argument(
        "url",
        type=str,
        default="https://staging.validation.linaro.org",
        help="base url",
    )
    parser.add_argument("config", type=pathlib.Path, help="configuration file")
    options = parser.parse_args()
    options.password = getpass()

    config = yaml.load(options.config.read_text(encoding="utf-8"))
    lava = LAVA(options)
    for conf in config["screenshots"]:
        lava(conf["name"], conf["actions"])


if __name__ == "__main__":
    sys.exit(main())

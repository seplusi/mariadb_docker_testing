from configparser import ConfigParser


class configClass(object):
    def __init__(self) -> None:
        self.data = ConfigParser()
        self.data.read('resources/objects/config/config.ini')

        """
        self.driver = driver
        self.config = config
        self.wait_driver = WebDriverWait(self.driver, explicit_wait)
        # Load page specific locators
        subfolder = 'mobile/' if 'mobile' in page_obj_class_name.lower() else ''
        self.config.read(f'resources/locator/{subfolder}{page_obj_class_name}.ini')
        self.locators = self._get_all_locators(page_obj_class_name)
        """
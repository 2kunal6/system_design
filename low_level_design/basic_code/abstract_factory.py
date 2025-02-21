from abc import ABC, abstractmethod

#--------------------------------------------------------------
class FormInterface(ABC):
    @abstractmethod
    def fill_form(self):
        pass
class WinForm(FormInterface):
    def fill_form(self):
        print('Filling Windows form')
class MacForm(FormInterface):
    def fill_form(self):
        print('Filling Mac form')

class DropdownInterface(ABC):
    @abstractmethod
    def choose_option(self):
        pass
class WinDropdown(DropdownInterface):
    def choose_option(self):
        print('choosing windows dropdown')
class MacDropdown(DropdownInterface):
    def choose_option(self):
        print('choosing mac dropdown')
#--------------------------------------------------------------
class AbstractFactory(ABC):
    @abstractmethod
    def create_form(self):
        pass

    @abstractmethod
    def create_dropdown(self):
        pass

class WinFactory(AbstractFactory):
    def create_form(self):
        return WinForm()

    def create_dropdown(self):
        return WinDropdown()

class MacFactory(AbstractFactory):
    def create_form(self):
        return MacForm()

    def create_dropdown(self):
        return MacDropdown()
#---------------------------------------------------------------

factory = WinFactory()
form = factory.create_form()
dropdown = factory.create_dropdown()

form.fill_form()
dropdown.choose_option()

factory = MacFactory()
form = factory.create_form()
dropdown = factory.create_dropdown()

form.fill_form()
dropdown.choose_option()

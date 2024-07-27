from textual.app import App
from textual.widgets import Static, Button


class App_(App):
    def on_mount(self):
        for obj in self.static():
            print(obj)

    def static(self):
        with Static():
            yield Button


if __name__ == '__main__':
    App_().run()


from .drop_downs import Components



class GetRadios:
    def __init__(self):
        self.instance = Components(
            on_server_change=self.on_server_change,
            on_tag_change=self.on_tag_change
        )

    def on_server_change(self, value):
        print("Server Qchanged:", value)

    def on_tag_change(self, value):
        print("TagQ changed:", value)

    def print_values(self):
        print("Current server value:", self.instance.server_value)
        print("Current tag value:", self.instance.tag_value)


    

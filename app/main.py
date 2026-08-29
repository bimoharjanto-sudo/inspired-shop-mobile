from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label


class InspiredShopApp(App):

    def build(self):
        layout = BoxLayout(
            orientation="vertical",
            padding=40,
            spacing=20
        )

        title = Label(
            text="INSPIRED SHOP",
            font_size="28sp",
            size_hint_y=None,
            height=80
        )

        tagline = Label(
            text="Happy Shopping!",
            font_size="20sp"
        )

        layout.add_widget(title)
        layout.add_widget(tagline)

        return layout


if __name__ == "__main__":
    InspiredShopApp().run()

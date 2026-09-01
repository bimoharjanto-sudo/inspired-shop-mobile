from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.metrics import dp


class InspiredShopApp(App):

    def build(self):
        root = BoxLayout(
            orientation="vertical",
            padding=dp(24),
            spacing=dp(14)
        )

        title = Label(
            text="INSPIRED SHOP",
            font_size="28sp",
            bold=True,
            size_hint_y=None,
            height=dp(60)
        )

        tagline = Label(
            text="Happy Shopping! 🛍️",
            font_size="18sp",
            size_hint_y=None,
            height=dp(40)
        )

        url_label = Label(
            text="Blog Product URL",
            font_size="16sp",
            halign="left",
            text_size=(None, None),
            size_hint_y=None,
            height=dp(30)
        )

        self.url_input = TextInput(
            hint_text="https://bjards.blogspot.com/...",
            multiline=False,
            size_hint_y=None,
            height=dp(52)
        )

        prompt_label = Label(
            text="Video Prompt",
            font_size="16sp",
            halign="left",
            size_hint_y=None,
            height=dp(30)
        )

        self.prompt_input = TextInput(
            hint_text="Masukkan prompt video atau gunakan prompt otomatis...",
            multiline=True,
            size_hint_y=None,
            height=dp(150)
        )

        generate_button = Button(
            text="✨ GENERATE PROMPT",
            font_size="16sp",
            size_hint_y=None,
            height=dp(52)
        )
        generate_button.bind(on_press=self.generate_prompt)

        render_button = Button(
            text="☁️ START CLOUD RENDER",
            font_size="16sp",
            size_hint_y=None,
            height=dp(58)
        )
        render_button.bind(on_press=self.start_render)

        status_label = Label(
            text="Status: Ready",
            font_size="16sp",
            size_hint_y=None,
            height=dp(45)
        )
        self.status_label = status_label

        root.add_widget(title)
        root.add_widget(tagline)
        root.add_widget(url_label)
        root.add_widget(self.url_input)
        root.add_widget(prompt_label)
        root.add_widget(self.prompt_input)
        root.add_widget(generate_button)
        root.add_widget(render_button)
        root.add_widget(status_label)

        return root

    def generate_prompt(self, instance):
        if not self.url_input.text.strip():
            self.status_label.text = "Status: Masukkan Blog URL terlebih dahulu"
            return

        self.prompt_input.text = (
            "Create a photorealistic cinematic commercial video "
            "using the product from the provided Blog URL as reference. "
            "Natural human movement, realistic lighting, premium lifestyle "
            "advertising aesthetic, smooth cinematic camera movement. "
            "Preserve product appearance and details."
        )
        self.status_label.text = "Status: Prompt generated ✓"

    def start_render(self, instance):
        if not self.url_input.text.strip():
            self.status_label.text = "Status: Masukkan Blog URL terlebih dahulu"
            return

        if not self.prompt_input.text.strip():
            self.status_label.text = "Status: Masukkan atau generate prompt terlebih dahulu"
            return

        self.status_label.text = "Status: Cloud Render — READY TO CONNECT ☁️"


if __name__ == "__main__":
    InspiredShopApp().run()

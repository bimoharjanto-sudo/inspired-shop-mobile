import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window

from cloud.render_client import CloudRenderClient


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

        self.status_label = Label(
            text="Status: Ready",
            font_size="16sp",
            size_hint_y=None,
            height=dp(45)
        )

        self.preview = Image(
            source="",
            size_hint_y=1,
            allow_stretch=True,
            keep_ratio=True,
        )

        root.add_widget(title)
        root.add_widget(tagline)
        root.add_widget(url_label)
        root.add_widget(self.url_input)
        root.add_widget(prompt_label)
        root.add_widget(self.prompt_input)
        root.add_widget(generate_button)
        root.add_widget(render_button)
        root.add_widget(self.status_label)
        root.add_widget(self.preview)

        return root

    def generate_prompt(self, instance):
        if not self.url_input.text.strip():
            self.status_label.text = (
                "Status: Masukkan Blog URL terlebih dahulu"
            )
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
        url = self.url_input.text.strip()
        prompt = self.prompt_input.text.strip()

        if not url:
            self.status_label.text = (
                "Status: Masukkan Blog URL terlebih dahulu"
            )
            return

        if not prompt:
            self.status_label.text = (
                "Status: Masukkan atau generate prompt terlebih dahulu"
            )
            return

        bridge_url = (
            os.environ.get(
                "AI_HUMAN_RENDER_BRIDGE_URL",
                "http://127.0.0.1:8765"
            ).strip().rstrip("/")
        )

        client = CloudRenderClient(base_url=bridge_url)

        self.status_label.text = "Status: Cloud Render — rendering... ☁️"

        scene = {
            "mode": "image",
            "image_prompt": prompt,
            "blog_url": url,
        }

        import threading

        thread = threading.Thread(
            target=self._render_worker,
            args=(client, scene),
            daemon=True,
        )
        thread.start()

    def _render_worker(self, client, scene):
        result = client.submit(scene)

        Clock.schedule_once(
            lambda dt: self._handle_render_result(result),
            0
        )

    def _handle_render_result(self, result):
        if result.get("status") != "success":
            message = result.get(
                "message",
                "Cloud Render gagal."
            )

            self.status_label.text = (
                f"Status: Render ERROR — {message}"
            )
            return

        output = result.get("output", "")

        if not output:
            self.status_label.text = (
                "Status: Render berhasil, tetapi output kosong."
            )
            return

        filename = output.replace("\\", "/").split("/")[-1]

        bridge_url = (
            os.environ.get(
                "AI_HUMAN_RENDER_BRIDGE_URL",
                "http://127.0.0.1:8765"
            ).strip().rstrip("/")
        )

        preview_url = (
            f"{bridge_url}/files/images/{filename}"
        )

        self.preview.source = preview_url
        self.preview.reload()

        self.status_label.text = (
            "Status: Render SUCCESS ✓"
        )


if __name__ == "__main__":
    InspiredShopApp().run()

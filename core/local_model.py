from pathlib import Path
import subprocess


class LocalModel:
    """
    رابط مدل زبانی محلی بی‌هوش.

    موتور اصلی در نسخه اندروید:
        llama.cpp

    مدل:
        Qwen3-1.7B-GGUF
    """

    def __init__(
        self,
        model_path="models/Qwen3-1.7B-Q8_0.gguf",
        llama_path="llama-cli"
    ):
        self.model_path = Path(model_path)
        self.llama_path = llama_path

    def available(self):
        return (
            self.model_path.exists()
            and self.model_path.is_file()
        )

    def ask(
        self,
        message,
        system_prompt=None,
        context_size=4096
    ):
        if not self.available():
            return (
                "مدل محلی هنوز نصب نشده است.\n\n"
                "فایل Qwen3-1.7B-Q8_0.gguf "
                "را در پوشه models قرار بده."
            )

        prompt_parts = []

        if system_prompt:
            prompt_parts.append(
                f"<|im_start|>system\n"
                f"{system_prompt}"
                f"\n<|im_end|>"
            )

        prompt_parts.append(
            f"<|im_start|>user\n"
            f"{message}"
            f"\n<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        prompt = "\n".join(prompt_parts)

        command = [
            self.llama_path,
            "-m",
            str(self.model_path),
            "-c",
            str(context_size),
            "-p",
            prompt,
            "--temp",
            "0.6",
            "--top-k",
            "20",
            "--top-p",
            "0.95",
            "-n",
            "1024",
        ]

        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=120
            )

            if result.returncode != 0:
                return (
                    "خطا در اجرای مدل محلی:\n\n"
                    + result.stderr
                )

            return result.stdout.strip()

        except subprocess.TimeoutExpired:
            return "اجرای مدل بیش از حد طول کشید."

        except Exception as error:
            return (
                "خطا در موتور مدل محلی:\n\n"
                f"{error}"
            )

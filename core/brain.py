from core.local_model import LocalModel
from search.web_search import WebSearch


class Brain:
    def __init__(self):
        self.name = "بی‌هوش"
        self.model = LocalModel()
        self.search = WebSearch()

    def needs_web_search(self, message):
        keywords = [
            "امروز", "الان", "جدیدترین", "آخرین",
            "قیمت", "اخبار", "خبر", "آب و هوا",
            "هوا", "ساعت", "تاریخ", "بازار",
            "نرخ", "دلار", "یورو", "بیت کوین",
            "بیت‌کوین", "اتریوم", "سایت",
            "اینترنت", "جستجو", "بررسی کن",
            "بررسی", "چه خبر",
            "latest", "today", "current",
            "news", "price"
        ]

        text = message.lower()
        return any(
            word.lower() in text
            for word in keywords
        )

    def format_search_results(self, results):
        if not results:
            return "نتیجه‌ای از اینترنت پیدا نشد."

        output = []

        for i, result in enumerate(results, 1):
            title = result.get("title", "")
            content = result.get("content", "")
            url = result.get("url", "")

            output.append(
                f"{i}. {title}\n"
                f"{content}\n"
                f"منبع: {url}"
            )

        return "\n\n".join(output)

    def local_answer(self, message):
        system_prompt = """
تو «بی‌هوش» هستی؛ یک دستیار هوش مصنوعی مستقل و محلی.

قوانین:
- فارسی را روان و طبیعی جواب بده.
- پاسخ‌ها را واضح و مفید بده.
- برای برنامه‌نویسی کد قابل اجرا ارائه کن.
- ادعا نکن به OpenAI متصل هستی.
- اگر چیزی را نمی‌دانی، صادقانه بگو.
"""

        return self.model.ask(
            message,
            system_prompt=system_prompt
        )

    def reply(self, message, history=None):
        message = message.strip()

        if not message:
            return "پیامت خالی است."

        lower = message.lower()

        if any(
            word in lower
            for word in ["سلام", "hello", "hi"]
        ):
            return (
                "سلام! 👾\n\n"
                "من بی‌هوش هستم.\n"
                "هسته مستقل من فعاله."
            )

        if "اسم" in message and "تو" in message:
            return "اسم من بی‌هوش است 👾"

        # جست‌وجوی اینترنت
        if self.needs_web_search(message):
            results = self.search.search(
                message,
                limit=5
            )

            return (
                "🌐 نتیجه جست‌وجوی اینترنت:\n\n"
                + self.format_search_results(results)
                + "\n\n"
                "🧠 بی‌هوش این اطلاعات را از اینترنت دریافت کرد."
            )

        # مدل زبانی محلی
        if self.model.available():
            return self.local_answer(message)

        # حالت موقت تا نصب مدل
        return (
            "🧠 هسته مستقل بی‌هوش فعال است.\n\n"
            f"پیامت:\n«{message}»\n\n"
            "🤖 مدل زبانی محلی هنوز نصب نشده است."
        )

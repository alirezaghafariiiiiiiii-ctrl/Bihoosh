from core.local_model import LocalModel
from search.web_search import WebSearch


class Brain:
    """
    هسته مستقل بی‌هوش.

    قابلیت‌ها:
    - مدل زبانی محلی
    - جست‌وجوی اینترنت
    - پاسخ پایه در صورت نبود مدل
    """

    def __init__(self):
        self.name = "بی‌هوش"

        self.model = LocalModel()
        self.search = WebSearch()

    def needs_web_search(self, message):
        keywords = [
            "امروز",
            "الان",
            "جدیدترین",
            "آخرین",
            "قیمت",
            "اخبار",
            "خبر",
            "آب و هوا",
            "هوا",
            "ساعت",
            "تاریخ",
            "بازار",
            "نرخ",
            "دلار",
            "یورو",
            "بیت کوین",
            "بیت‌کوین",
            "اتریوم",
            "کجا",
            "سایت",
            "اینترنت",
            "جستجو",
            "بررسی کن",
            "بررسی",
            "چه خبر",
            "latest",
            "today",
            "current",
            "news",
            "price",
        ]

        text = message.lower()

        return any(
            keyword.lower() in text
            for keyword in keywords
        )

    def format_search_results(self, results):
        if not results:
            return "نتیجه‌ای از اینترنت پیدا نشد."

        output = []

        for i, result in enumerate(results, 1):
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")

            output.append(
                f"{i}. {title}\n"
                f"{content}\n"
                f"منبع: {url}"
            )

        return "\n\n".join(output)

    def local_answer(self, message):
        """
        پاسخ توسط مدل محلی.
        """

        system_prompt = """
تو «بی‌هوش» هستی؛ یک دستیار هوش مصنوعی مستقل و محلی.

قوانین:
- فارسی را روان و طبیعی جواب بده.
- کوتاه و مفید جواب بده مگر اینکه کاربر توضیح کامل بخواهد.
- برای برنامه‌نویسی کد دقیق و قابل اجرا بده.
- ادعا نکن به OpenAI وصل هستی.
- اگر اطلاعاتی را نمی‌دانی، صادقانه بگو.
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

        # پاسخ‌های خیلی ساده بدون نیاز به مدل
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

            search_text = self.format_search_results(
                results
            )

            return (
                "🌐 نتیجه جست‌وجوی اینترنت:\n\n"
                + search_text
                + "\n\n"
                "🧠 بی‌هوش این اطلاعات را از اینترنت دریافت کرد."
            )

        # مدل محلی
        if self.model.available():
            return self.local_answer(message)

        # حالت موقت تا زمانی که مدل نصب شود
        return (
            f"پیامت را دریافت کردم:\n\n"
            f"«{message}»\n\n"
            "🧠 هسته مستقل فعال است.\n"
            "🌐 جست‌وجوی اینترنت فعال است.\n"
            "🤖 مدل زبانی محلی هنوز نصب نشده است."
        )

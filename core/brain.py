class Brain:
    """
    هسته اصلی بی‌هوش.

    فعلاً یک موتور پایه است.
    در مرحله بعد مدل زبانی محلی به همین کلاس متصل می‌شود.
    """

    def __init__(self):
        self.name = "بی‌هوش"

    def reply(self, message, history=None):
        message = message.strip()

        if not message:
            return "پیامت خالی است."

        lower = message.lower()

        if any(word in lower for word in [
            "سلام",
            "hello",
            "hi"
        ]):
            return "سلام! 👾 من بی‌هوش هستم. آماده‌ام."

        if "اسم" in message and "تو" in message:
            return "اسم من بی‌هوش است 👾"

        return (
            f"پیامت را دریافت کردم: «{message}»\n\n"
            "هسته مستقل من آماده است. "
            "در مرحله بعد موتور مدل زبانی محلی "
            "به من متصل می‌شود."
        )

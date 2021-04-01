class StringHelpers:
    """description of class"""

    @staticmethod
    def strip_end(text, suffix, removeLen):
        value = text
        try:
            if text.endswith(suffix):
                value = text[:len(text) - removeLen]
        except Exception as ex:
            print("StringHelpers: strip_end: " + ex)
        return value



MARKDOWN_CHARS_TO_ESC = {"*": "\\*", "_": "\\_", "~": "\\~", "`": "\\`", ">": "\\>"}


def get_latency_ms(bot):
    return round(bot.latency * 1000, 1)


def escape_from_md(content):
    if len(content.strip()) == 0:
        # Only whitespace
        return content.strip()
    for charset in MARKDOWN_CHARS_TO_ESC.items():
        content = content.replace(*charset)
    return content

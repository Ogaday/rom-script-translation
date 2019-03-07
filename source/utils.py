def annotated(source_text):
    outtext = source_text.replace(
            '{', '<div class="notranslate">{'
        ).replace(
            '}', '}</div>'
        )
    return outtext


def deannotated(source_text):
    outtext = source_text.replace(
            '<div class="notranslate">', ""
        ).replace(
            "</div>", ""
        )
    return outtext

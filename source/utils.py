import re


def annotated(source_text):
    outtext = source_text.replace(
            '{', '<div class="notranslate">{'
        ).replace(
            '}', '}</div>'
        )
    return outtext


def deannotated(source_text):
    outtext = re.sub(
            r' ?<div class="notranslate"> ?',
            '',
            re.sub(
                r' ?</div> ?',
                r'',
                source_text
            )
        )
    return outtext

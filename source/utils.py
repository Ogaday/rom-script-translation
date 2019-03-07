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


def paginate(lines, max_buffer, max_lines):
    """
    Iterate chunks of lines so chunks don't exceed a buffer or line limit
    """
    start = 0
    stop = 0

    while stop < len(lines):
        if len(lines[stop]) > max_buffer:
            raise Exception('A line is too long')

        buffer_size = len(''.join(lines[start:stop + 1]))
        num_lines = len(lines[start:stop + 1])
        if buffer_size > max_buffer or num_lines > max_lines:
            yield lines[start:stop]
            start = stop
        stop += 1
    else:
        yield lines[start:stop]

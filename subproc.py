#!/usr/bin/env python

# TODO: record history and map arrow keys to navigating it
# TODO: configuration file to load palette, shell, etc.
# TODO: what to do about ctrl-l for clearing the screen
# TODO: ctrl-c handling
# TODO: fix output mingling between commands by using different widgets?

import functools
import subprocess
import urwid
import os
import sys

palette = [
    ('spacer', 'white', 'white'),
    ('stdout', 'black', 'white'),
    ('stderr', 'light red', 'white'),
    ('command', 'black', 'light gray'),
    ('error', 'light red', 'black'),
]

output_widget = urwid.Text(markup='')
prompt_widget = urwid.Edit("$ ")
frame_widget = urwid.Frame(
    header=prompt_widget,
    body=urwid.Filler(output_widget, valign='top'),
    focus_part='header',
)

def on_enter(key):
    if key == 'enter':
        cmd = prompt_widget.text
        cmd = cmd.lstrip('$ ')
        if cmd == 'exit':
            raise urwid.ExitMainLoop()
        extend_text(output_widget, 'command', cmd + '\n')
        stdout_fd = loop.watch_pipe(
            functools.partial(
                received_output,
                style='stdout',
            )
        )
        stderr_fd = loop.watch_pipe(
            functools.partial(
                received_output,
                style='stderr',
            )
        )
        proc = subprocess.Popen(
            cmd,
            stdout=stdout_fd,
            stderr=stderr_fd,
            close_fds=True,
            shell=True,
            executable='/bin/bash',
        )
        prompt_widget.set_edit_text('')

    elif key == 'ctrl d':
        raise urwid.ExitMainLoop()

    elif key == 'ctrl l':
        # Muscle memory trying to clear the screen. Ignore.
        pass

    elif key in ('left', 'right', 'backspace'):
        # Trying to move past the edges of the input text when
        # editing. Ignore.
        pass
    else:
        extend_text(output_widget, 'error',
                    'Unknown keypress {!r}'.format(key))


def extend_text(widget, style, text):
    existing = widget.get_text()
    parts = []
    start = 0
    existing_text = existing[0]
    for attr, count in existing[1]:
        parts.append((attr, existing_text[start:start+count]))
        start += count
    if style == 'command':
        # insert a new command entry and an empty stdout entry, in
        # reverse order because we're pushing them onto the front of
        # the list
        parts.insert(0, ('stdout', ''))
        parts.insert(0, ('stderr', ''))
        parts.insert(0, (style, text))
        parts.insert(0, ('spacer', '\n'))
    elif style == 'error':
        parts.insert(0, (style, text.rstrip() + '\n'))
    elif style in ('stdout', 'stderr'):
        # Append to the most recently added block of the right style.
        loc = None
        for i, p in enumerate(parts):
            if p[0] == style:
                loc = i
                break
        else:
            raise RuntimeError('did not find stdout block')
        new_text = parts[loc][1] + text
        parts[loc] = (parts[loc][0], new_text)
    else:
        raise ValueError('unknown style {} used for {!r}'.format(style, text))
    widget.set_text(parts)


def received_output(data, style):
    extend_text(output_widget, style, data.decode('utf-8'))


loop = urwid.MainLoop(
    frame_widget,
    unhandled_input=on_enter,
    palette=palette,
)

loop.run()

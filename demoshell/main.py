#!/usr/bin/env python

# TODO: record history and map arrow keys to navigating it
# TODO: configuration file to load palette, shell, etc.
# TODO: what to do about ctrl-l for clearing the screen
# TODO: ctrl-c handling
# TODO: fix output mingling between commands by using different widgets?
# TODO: allow the config file to define new builtins
# TODO: allow the config file to define aliases to handle the "ll" case
# TODO: figure out how to map ctrl-l to clear

import functools
import subprocess
import urwid
import os
import sys


class DemoShell:

    palette = [
        ('spacer', 'white', 'white'),
        ('stdout', 'black', 'white'),
        ('stderr', 'light red', 'white'),
        ('command', 'black', 'light gray'),
        ('error', 'light red', 'black'),
    ]

    def __init__(self):
        self.output_widget = urwid.Text(markup='')
        self.prompt_widget = urwid.Edit("$ ")
        self.frame_widget = urwid.Frame(
            header=self.prompt_widget,
            body=urwid.Filler(self.output_widget, valign='top'),
            focus_part='header',
        )
        self._builtins = {
            'exit': self._exit,
            'clear': self._clear,
        }

    def run(self):
        self.loop = urwid.MainLoop(
            self.frame_widget,
            unhandled_input=self.on_enter,
            palette=self.palette,
        )
        self.loop.run()

    def _exit(self):
        raise urwid.ExitMainLoop()

    def on_enter(self, key):
        if key == 'enter':
            cmd = self.prompt_widget.text
            cmd = cmd.lstrip('$ ')
            if cmd in self._builtins:
                self._builtins[cmd]()
            elif cmd:
                self._run_external_command(cmd)
            self.prompt_widget.set_edit_text('')

        elif key == 'ctrl d':
            self._exit()

        elif key in ('left', 'right', 'backspace'):
            # Trying to move past the edges of the input text when
            # editing. Ignore.
            pass

        else:
            self.extend_text(
                'error',
                'Unknown keypress {!r}'.format(key),
            )

    def _run_external_command(self, cmd):
        self.extend_text('command', cmd + '\n')
        stdout_fd = self.loop.watch_pipe(
            functools.partial(
                self.received_output,
                style='stdout',
            )
        )
        stderr_fd = self.loop.watch_pipe(
            functools.partial(
                self.received_output,
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

    def _clear(self):
        self.output_widget.set_text('')

    def extend_text(self, style, text):
        existing = self.output_widget.get_text()
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
            raise ValueError('unknown style {} used for {!r}'.format(
                style, text))
        self.output_widget.set_text(parts)

    def received_output(self, data, style):
        self.extend_text(style, data.decode('utf-8'))


def main():
    DemoShell().run()

if __name__ == '__main__':
    main()

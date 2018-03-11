============
 Demo Shell
============

``demoshell`` is a simplified shell for live demonstrations. It always
shows the command prompt at the top of the screen and pushes command
output down instead of letting iscroll up.

Huh?
====

POSIX shells print their output in such a way that it scrolls up and
off the top of the screen because they are using tty semantics, which
are based on hardware that used to literally print everything on a
roll of paper that moved up through the machine and over the top.

It's the 21st century. We don't use paper-based terminals any
more. While continuing to pretend we do is fine for day-to-day work,
when we are giving live presentations it is not ideal because the most
interesting thing you are doing is probably at the bottom of your
screen during a live demo. That is the hardest part of the screen for
people at the back of the room to see, because it is often blocked by
other people's heads.

``demoshell`` avoids this problem by always keeping the command prompt
at the top of the screen and showing the output of commands below,
pushing older commands off of the bottom of the screen to make space
for newer text.

Using demoshell
===============

Install the shell with ``pip3`` (it works best under Python 3)::

  $ pip3 install demoshell

Run ``demoshell``::

  $ demoshell

Run any shell command at the prompt::

  $ ls

  ls
  AUTHORS
  ChangeLog
  LICENSE
  README.rst
  demoshell
  demoshell.egg-info
  dist
  requirements.txt
  setup.cfg
  setup.py
  test

Use ``exit`` or ``Ctrl-D`` to leave the shell.

Use ``clear`` to clear the screen.

Resources
=========

* GitHub: https://github.com/dhellmann/demoshell
* Bugs: https://github.com/dhellmann/demoshell/issues
* Documentation: *Help wanted!*

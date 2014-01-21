##############################################
LICENSE
##############################################
GNU LIBRARY GENERAL PUBLIC LICENSE
Version 2, June 1991

Copyright (C) 1991 Free Software Foundation, Inc.
59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
Everyone is permitted to copy and distribute verbatim copies
of this license document, but changing it is not allowed.

[This is the first released version of the library GPL.  It is
numbered 2 because it goes with version 2 of the ordinary GPL.]

##############################################
README
##############################################
This directory contains source code of gmidimonitor program.

Go to http://home.gna.org/gmidimonitor/ for more info.

See INSTALL for info how to build/install the program.

=== Using GMIDImonitor ===
You need to connect desired source of MIDI events to gmidimonitor
input using some kind of patchbay like qjackctl, patchage or
gladish.

##############################################
INSTALL
##############################################
Quick instructions: ./waf configure && ./waf && sudo ./waf install

You need:

  1. Build tools
     1.1 compiler + linker
         Known to work with gcc 3.4.3 and binutils 2.15.94.0.2.2
         You can get gcc from http://www.gnu.org/software/gcc/
         You can get binutils from http://www.gnu.org/software/binutils/
     1.2 Python
         Known to work with Python 2.7.1
         You can get it from http://www.python.org/
     1.3 pkg-config
         Known to work with pkg-config 0.19
         You can get it from http://pkgconfig.freedesktop.org/wiki/

  2. Libraries
     2.1 GTK+ >= 2.12 (required)
         Known to work with GTK+ 2.24.4
         You can get it from http://www.gtk.org/
     2.2 JACK with MIDI support, i.e. >= 0.102.20 (optional)
         You can get it from http://jackaudio.org/
     2.3 ALSA library (optional)
         Known to work with alsa-lib 1.0.9
         You can get it from http://www.alsa-project.org/
     2.4 LASH (optional)
         Known to work with lash 0.5.0
         You can get it from http://www.nongnu.org/lash/

Support for both JACK MIDI and ALSA MIDI is optional, but you have
to use at least one of them.

To configure gmidimonitor execute the configure script:

    # ./waf configure

If you want to explicitly enable or disable jack, alsa or lash
support, you can do it at configure stage.

For example:

    # ./waf configure --alsa=no --jack=yes

With these options, the configure stage will not even try to detected
whether ALSA can be built, will fail if JACK it cannot find JACK and
will enable LASH only if it is available.

To build gmidimonitor:

    # ./waf

Now install it (you may need to be root to do this):

    # ./waf install

Good luck and report bugs so they can get fixed.

Usermin SSH-Authkey module
==========================

A simple [Usermin](http://webmin.com/usermin.html) module,
providing restricted modified to users' `authorized_keys` file.

Unlike the standard
[SSH configuration](http://doxfer.webmin.com/Webmin/SSH_Configuration)
module, this module allows only adding simple SSH keys, without
any additional options (such as custom commands or forwarding options).

Adding new keys is simpler, as the user just needs to copy&paste
the content of the public key - the module will parse and validate it
before adding it to the file.

This module is suitable if your SSH environment is restricted
(e.g. chroot or restricted shell) - and you only want to allow users
to change keys, but not other options (there is no way to configure
the standard usermin SSH module to restrict the user).

See screen shots at <https://housegordon.org/usermin-sshauth/>.

Download WBM file at <https://housegordon.org/usermin-sshauth/sshauth.wbm.gz>.

Code available at: <https://github.com/agordon/usermin-sshauth>.

Copyright (C) 2016 Assaf Gordon <assafgordon@gmail.com>.

License: BSD-3-Clause (same as usermin itself).

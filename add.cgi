#!/usr/bin/env perl
#
# SSH Auth - A usermin module for simple editing of
#            SSH authorizedkeys file
#
# Copyright (C) Assaf Gordon <assafgordon@gmail.com>
# License: BSD-3-Clause license
#          (Same as usermin - see <usermin>/LICENSE file)
#
# add.cgi - allow user to paste a add a new key.
# Based on <usermin>/ssh/edit_auth.cgi file.

require './sshauth-lib.pl';
&ReadParse();

&ui_print_header(undef, $text{'sshauth_add_title'}, "");

print $text{'sshauth_add_desc'}, "\n";

print &ui_form_start("save.cgi", "post");

print &ui_hidden("new", 1),"\n";

print &ui_table_start($text{'auth_new_header'}, "width=70%", 2);

print &ui_table_row($text{'sshauth_key_content'},
                    &ui_textarea("key", "", 15, 50, "on"));

print &ui_table_end();

print &ui_form_end([ [ "create", $text{'sshauth_btn_add_this_key'} ] ]);

&ui_print_footer("", $text{'index_return'});

#!/usr/bin/env perl
#
# SSH Auth - A usermin module for simple editing of
#            SSH authorizedkeys file
#
# Copyright (C) Assaf Gordon <assafgordon@gmail.com>
# License: BSD-3-Clause license
#          (Same as usermin - see <usermin>/LICENSE file)
#
# index.cgi - list available keys
# Based on <usermin>/ssh/list_auth.cgi file.

require './sshauth-lib.pl';

&ui_print_header(undef, $text{'sshauth_title'}, "");

print $text{'sshauth_desc'}, "<p>\n";

@auths = &list_user_authorized_keys();

if (@auths) {
	print &ui_columns_start([ $text{'sshauth_key_name'},
				  $text{'sshauth_key_type'},
				  $text{'sshauth_key_length'},
				  $text{'sshauth_key_fingerprint'},
				  $text{'sshauth_key_opts'},
				  $text{'sshauth_key_last_digits'}
                                ]);

	foreach $a (@auths) {
            @rows = ( "<a href='view.cgi?idx=$a->{'index'}'>".
                      "$a->{'name'}</a>" );

            if ($a->{'valid'}) {
                push @rows, (
                    $a->{'key_type'},
                    $a->{'key_length'},
                    $a->{'key_fingerprint'},
                    ( $a->{'opts'} ? "Yes" : "")
                );
            }
            else {
                push @rows, '(' . $text{'sshauth_invalid_key'} .')',"","","";
            }

            push @rows, '...' . substr($a->{key},-20);

            print &ui_columns_row(\@rows);

        }

	print &ui_columns_end();
	}
else {
	print '<b>' . $text{'sshauth_no_keys_found'} . "</b><p>\n";
     }

# Show a button for "create new key".
# This looks better (and more user-friendly) then an <a> link.
print &ui_form_start("add.cgi", "get");
print &ui_form_end([ [ "new", $text{'sshauth_btn_add'} ] ]);

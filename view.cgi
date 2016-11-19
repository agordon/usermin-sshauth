#!/usr/bin/env perl
#
# SSH Auth - A usermin module for simple editing of
#            SSH authorizedkeys file
#
# Copyright (C) Assaf Gordon <assafgordon@gmail.com>
# License: BSD-3-Clause license
#          (Same as usermin - see <usermin>/LICENSE file)
#
# view.cgi:
#   Display the content of a selected key,
#   with a 'delete' buttom.

require './sshauth-lib.pl';
&ReadParse();

$index = $in{'idx'};

@auths = &list_user_authorized_keys();
if (!@auths) {
    # No auth keys for this user? bail out
    &redirect("index.cgi");
    exit;
}

$auth = $auths[$index];
if (!$auth) {
    # Invalid index requested - bail out
    &redirect("index.cgi");
    exit;
}

&ui_print_header(undef, $text{'sshauth_view_title'}, "");

# Show main key details
print $text{'sshauth_view_desc'}, "\n";

# The only allowed operation is to delete this key
print &ui_form_start("save.cgi", "post");
print &ui_hidden("idx", $index),"\n";
print &ui_hidden("delete",1),"\n";

print &ui_table_start($text{'auth_header'}, "width=70%", 2);

print &ui_table_row( $text{'sshauth_key_name'}, $auth->{'name'});

print &ui_table_row( $text{'sshauth_key_type'}, $auth->{'key_type'});

print &ui_table_row( $text{'sshauth_key_length'}, $auth->{'key_length'});

print &ui_table_row( $text{'sshauth_key_fingerprint'}, $auth->{'key_fingerprint'});

print &ui_table_row( $text{'sshauth_key_valid'}, $auth->{'valid'} ? 'yes' : 'no');

print &ui_table_row( $text{'sshauth_key_digits'},
	&ui_textarea("key", $auth->{'key'}, 10, 50, "on", 0, "readonly"), 3);

# Show key options
if ($auth->{'opts'}) {
    &parse_options($auth->{'opts'}, \%opts);

    print &ui_table_hr();

    print &ui_table_row("",$text{'sshauth_key_options_desc'});

    foreach $optname (sort keys %opts) {
        print &ui_table_row($optname, join("<br/>", @{$opts{$optname}} ) );
    }
}

print &ui_table_end();

print &ui_form_end([ [ "delete", $text{'sshauth_btn_delete'} ] ]);

&ui_print_footer("", $text{'index_return'});

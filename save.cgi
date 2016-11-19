#!/usr/bin/env perl
#
# SSH Auth - A usermin module for simple editing of
#            SSH authorizedkeys file
#
# Copyright (C) Assaf Gordon <assafgordon@gmail.com>
# License: BSD-3-Clause license
#          (Same as usermin - see <usermin>/LICENSE file)
#
# save.cgi - add or delete a key
# Based on <usermin>/ssh/save_auth.cgi file.
#
# This module has no gui. It only handles <FORM> post requested
# from either the 'add.cgi' or 'view.cgi' modules.
#
# If the user is adding a new key, perform validation
# before adding the key.
# The validation is limited on purpose: we only accept
# simple SSH pubkeys, without any options.
#
require './sshauth-lib.pl';

&ReadParse();


# Delte request - delete the key and exit
if ( $in{'delete'} ) {
    local $idx = $in{'idx'};
    &delete_auth_key($idx);
    &redirect("index.cgi");
    exit;
}

# Not 'delete' and not 'new'? - bail out.
if (!$in{'new'}) {
    &redirect("index.cgi");
    exit;
}


## Add new key, after validation

# Setup Error reporting (if needed)
&error_setup($text{'sshauth_add_err_title'});

$key = $in{'key'};
&error($text{'sshauth_add_err_empty_key'}) unless $key;

# Remove any non-ascii, then non-printable characters
$key =~ s/^\s+//g;
$key =~ s/\s+$//g;
$key =~ s/[^[:ascii:]]//g;
$key =~ s/[^[:print:]]//g;

# Remove any newlines (if users copy&paste from terminal)
$key =~ s/[\r\n]//g;

($type,$digits,$name) = split /\s+/, $key;

$valid_type   = $type =~ /^ssh-[a-z]+$/;
$valid_digits = $digits =~ /^[a-z0-9\+\/=]+$/i;
$valid_name = length($name)>0;

&error($text{'sshauth_add_err_invalid_type'} . "<code>$type</code>")
    unless $valid_type;
&error($text{'sshauth_add_err_invalid_digits'} . "<code>$digits</code>")
    unless $valid_type;

# regardless of what the original string had,
# generate a new one containing only 3 valid fields
$key = join(" ", $type, $digits, $name);

if ($valid_type && $valid_digits && $valid_name) {
    ($valid_fingerprint, $key_len, $key_fingerprint, $key_name, $key_type) =
        get_ssh_key_finger_print ($key);
}

&error($text{'sshauth_add_err_invalid_fingerprint'} . "<code>$key</code>")
    unless $valid_fingerprint;


## DEBUG
if (0) {
    &ui_print_header(undef, "Save Key - DEBUG", "");

    print<<"EOF";
    <pre>
DEBUG MODE (not not added)

CGI Parameter:
  key = '$key'

Parsed Values:
  type = '$type'
  digits = '$digits'
  name = '$name'

ssh-keygen returned:
  key_len = $key_len
  key_fingerprint = $key_fingerprint
  key_name = $key_name
  key_type = $key_type

valid_type = $valid_type
valid_digits = $valid_digits
valid_name = $valid_name

valid_fingerprint = $valid_fingerprint
</pre>
EOF
exit;
}


## Add the key
add_auth_key($key);

&redirect("index.cgi");

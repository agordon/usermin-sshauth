# SSH Auth - A usermin module for simple editing of
#            SSH authorizedkeys file
#
# Copyright (C) Assaf Gordon <assafgordon@gmail.com>
# License: BSD-3-Clause license
#          (Same as usermin - see <usermin>/LICENSE file)
#
# sshauth-lib.pl -
# Common functions for manipulating the users .ssh/authorized_key files
# Based on <usermin>/ssh/ssh-lib.pl file.

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();
&switch_to_remote_user();

$ssh_directory = "$remote_user_info[7]/.ssh";
$authorized_keys = "$ssh_directory/authorized_keys";

=pod
get_ssh_key_finger_print():

given a string of an ssh public key, saves the string to a temp file
and runs 'ssh-keygen -l -f FILE'.

Returns a list of 5 items:
   valid: 1=yes, 0=no.  If not valid, all other fields should be ignored.
   len:   a numeric value (or string), as returned from 'ssh-keygen -l'.
   fingerprint: a colon-separated list of hex digits.
   name:  name as returned from ssh-keygen.
   type:  type as returned from ssh-keygen.

Example:
   @a = get_ssh_key_finger_print("ssh-rsa AAAAAA[...]AFDSAFDSA== foobar@example.com")
returns:
   $a[0] = 1
   $a[1] = "2048"
   $a[2] = "00:12:32:ba:43:23:12:31:43:54:54:56"
   $a[3] = "foobar@example.com"
   $a[4] = "(RSA)"

=cut
sub get_ssh_key_finger_print
{
    local $key = shift;
    local $fn = transname("sshauthkey");
    open(F,'>',$fn) or die "failed to open temp file '$fn': $!";
    print F $key;
    close (F) or die "failed to close/write temp file '$fn': $!";

    local $kfp = backquote_logged("ssh-keygen -l -f '$fn'");
    local $rc = $?;
    chomp $kfp;
    local ($len, $fingerprint, $name, $type) = split /\s+/, $kfp;

    $len = '' unless defined $len;
    $fingerprint = '' unless defined $fingerprint;
    $name = '' unless defined $name;
    $type = '' unless defined $type;

    local $valid = (($rc==0)
                    &&
                    ($len =~ /^\d+$/)
                    &&
                    ($fingerprint =~ /^[0-9a-f:]+$/)
                    &&
                    ($type =~ /^\([\w]+\)$/i)) ? 1 : 0;

    return ($valid, $len, $fingerprint, $name, $type);
}


=pod
list_user_authorized_keys()

Returns a list of authorized key structures.

This function reads the user's "$HOME/./ssh/authorizedkeys" file,
and returns a list (one item per key).

ONLY SSH2 keys are returned. SSH1 keys are ignored.

Each item in the list is a hash containing:

    {
      'name' => name of key (last field in each key)
      'key'  => Base64 content of the key
      'opts' => any additional options for the key
                (e.g. commands / hosts / pty / forwardning)
      'keytype' => e.g. 'ssh-rsa' or 'ssh-dsa'
      'type' => always 2 (for SSH2 key)
      'line' => line number in the authorizedkeys file
      'index' => 0-based index of this key in the list

     The following keys are returned from get_ssh_key_finger_print:
      'valid' => 1 or 0
      'key_length'
      'key_fingerprint'
      'key_type' => e.g. '(RSA)' or '(DSA)'
    }
=cut

sub list_user_authorized_keys
{
local @rv;
local $lnum = 0;
open(AUTHS, $authorized_keys);
while(<AUTHS>) {
	s/\r|\n//g;
	s/#.*$//;
	if (/^((.*)\s+)?(\d+)\s+(\d+)\s+(\d+)\s+(\S+)$/) {
		# SSH1 style line - ignored
		}
	elsif (/^((.*)\s+)?([a-z]\S+)\s+(\S+)\s+(\S+)/) {
		# SSH2 style line
		local $auth = { 'name' => $5,
				'key' => $4,
				'opts' => $2,
				'keytype' => $3,
				'type' => 2,
				'line' => $lnum,
				'index' => scalar(@rv) };
		$auth->{'opts'} =~ s/\s+$//;

                # Get the key's fingerprint, ignoring any options
                local $keyline = "$3 $4 $5";
                local ($valid, $len, $fp, $name, $type) =
                    get_ssh_key_finger_print($keyline);

                $auth->{'valid'} = $valid;
                $auth->{'key_length'} = $len;
                $auth->{'key_fingerprint'} = $fp;
                $auth->{'key_type'} = $type;

		push(@rv, $auth);
		}
	$lnum++;
	}
close(AUTHS);
return @rv;
}


=pod
add_auth_key()

Given a string, adds it as a new line to the user's authorizedkeys file.
The line is added as-is, no validation is performed.
=cut
sub add_auth_key
{
local $lref = &read_file_lines($authorized_keys);
push(@$lref, $_[0]);
&flush_file_lines();
}

=pod
delete_auth_key()

Remove a line (by line index number, 0=first line)
from user user authorrizedkeys file.
=cut
sub delete_auth_key
{
local $lref = &read_file_lines($authorized_keys);
splice(@$lref, $_[0], 1);
&flush_file_lines();
}


=pod
parse_options(string, &opts)

Parses the 'opts' value from the user's authoriedkeys file.
The input should be the 'opt' value as returned by
list_user_authorized_keys().

This function was copied as-is from usermin's "ssh/ssh-lib.pl" file.

=cut
sub parse_options
{
local $opts = $_[0];
while($opts =~ /^([^=\s,]+)=\"([^\"]*)\",?(.*)$/ ||
      $opts =~ /^([^=\s,]+)=([^=\s,]+),?(.*)$/ ||
      $opts =~ /^([^=\s,]+)(),?(.*)$/) {
	push(@{$_[1]->{$1}}, $2);
	$opts = $3;
	}
}

1;

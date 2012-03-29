#!/usr/bin/perl -w


sub help(){
	print "\n";
	print "whitelist2ldap.pl client|recipient DN whitelist-file\n";
	print "\twhitelist2ldap.pl client ou=postgreyldap,dc=yoursite,dc=com postygrey_whitelist_client\n";
	print "\twhitelist2ldap.pl reciepients ou=postgreyldap,dc=yoursite,dc=com postygrey_whitelist_recipients\n\n";
	print "\tWill read in postgrey whitelists and attempt to produce reasonable LDAP equivalents.\n";
	print "\tMakes many assumptions about the input file WRT comments and such.\n";
	print "\n";
	exit;
}

my $mode = shift || help();
my $dn = shift || help();
my $file = shift || help();


help() unless ($mode eq "client" || $mode eq "recipient");

unless (-f $file) {
	print "File not found, dummy\n\n";
	exit;
}
print "mode: $mode dn: $dn file: $file\n";

sub writeEntry($$) {
	my ($comment, $entry) = @_;
	print "Writing entry: $entry with comment: $comment\n";

	my $cn = $entry;
	$cn =~ s/,/2C/g;
	$cn =~ s/\+/2B/g;
	$cn =~ s/"/22/g;
	$cn =~ s/\\/5C/g;
	$cn =~ s/</3C/g;
	$cn =~ s/>/3E/g;
	$cn =~ s/;/3B/g;
	$cn =~ s/=/3D/g;
	$cn =~ s/\//2F/g;

	#smash non-printable ASCII characters. Should work in Description, but apparently not always.
	$comment =~ s/[\x80-\xFF]+//g;
	my $desc = ""; 
	$desc = "Description: $comment" if ($comment);
	
	my $objectClass;
	if ($mode eq "client") {
		$objectClass = "GreyListClientWhitelist"
	} else {
		$objectClass = "GreyListRecipientWhitelist"
	}
	
	print OUTPUT << "EOF"
dn: cn=$cn,$dn
objectClass: $objectClass
cn: $cn
PostgreyWhitelistEntry: $entry
Description: Was imported from files
$desc

EOF

}

open(INPUT, "<$file") || die(@!);
open(OUTPUT, ">import-$mode.ldif") || die(@!);

my $location = "comment";
my ($lastcomment, $lastentry);

while (<INPUT>) {
	print ">> $_";
	if ($location eq "comment") {
		if (/^#(.+)/) {
			$lastcomment = $1;
		} elsif (/^(\s?+)$/) {
			$lastcomment = "";
		} elsif (/^(.+)\s?+#?/) {
			$lastentry = $1;
			writeEntry($lastcomment, $lastentry);
		} else {
			die ("I'm not smart enough to process your file");
		}
	}
}

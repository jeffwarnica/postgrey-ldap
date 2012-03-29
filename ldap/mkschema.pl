#!/usr/bin/perl

`rm -rf ldif_output` if -d "ldif_output";
`rm schema_convert.conf` if -f "schema_convert.conf";

`echo "include schema.ldif" > schema_convert.conf`;

mkdir "ldif_output";

`/usr/sbin/slaptest -f schema_convert.conf -F ldif_output`;

open(IN, '<ldif_output/cn=config/cn=schema/cn={0}schema.ldif');
open(OUT, '> schema4ldapadd.ldif');

while(<IN>) {
	s/#.*//;            # ignore comments by erasing them
        next if /^(\s)*$/;  # skip blank lines
        s/(\{\d+\})//g;
        s/dn: cn=schema/dn: cn=postgreyldap,cn=schema,cn=config/;
        next if (/structuralObjectClass:/);
        next if (/entryUUID:/);
        next if (/creatorsName:/);
        next if (/createTimestamp:/);
        next if (/entryCSN:/);
        next if (/modifiersName:/);
        next if (/modifyTimestamp:/);
        
	print OUT $_;
}
print OUT "cn: postgreyldap\n";

close IN;
close OUT;
`rm -rf ldif_output`;
`rm schema_convert.conf`;

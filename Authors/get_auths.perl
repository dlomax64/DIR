use strict;
use warnings;

my $i = $ARGV[0];
my %auths = ();

my $file = 'zcat /da3_data/basemaps/gz/c2datFullT' . $i . '.s|';
my $output = 'authors.' . $i . '.out';

open A, $file or die $!;
open B, '>>', $output or die $!;
while(<A>) {
  chop();

  my @contents = split(/;/);
  my $auth = $contents[3];
  my $commit = $contents[0];
  if(not $auth) { next; }

  #if(not exists $auths{$auth}{"commits"}{$commit}) { $auths{$auth}{"commits"} = $commit; }
  $auths{$auth} = $commit;
}

while( my($key, $value) = each %auths ) {
  print B "$key;$value\n"
}

close A;
close B;

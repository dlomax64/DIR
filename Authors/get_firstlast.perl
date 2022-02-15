use strict;
use warnings;

my $i = $ARGV[0];
my %auths = ();

my $file = 'zcat /da3_data/basemaps/gz/c2datFullT' . $i . '.s|';
my $output = 'timeline.' . $i . '.out';

open A, $file or die $!;
open B, '>>', $output or die $!;

while(<A>) {
  chop();

  my @contents = split(/;/);
  my $commit = $contents[0];
  my $time = $contents[1];
  my $auth = $contents[3];

  if(not $auth) { next; }

  if (not exists $auths{$auth}) {
    $auths{$auth}{"earliest"} = $time;
    $auths{$auth}{"e_commit"} = $commit;
    $auths{$auth}{"latest"} = $time;
    $auths{$auth}{"l_commit"} = $commit;
  } 
  elsif ($auths{$auth}{"earliest"} gt $time) {
    $auths{$auth}{"earliest"} = $time;
    $auths{$auth}{"e_commit"} = $commit;
  }
  elsif ($auths{$auth}{"latest"} lt $time) { 
    $auths{$auth}{"latest"} = $time;
    $auths{$auth}{"l_commit"} = $commit;
  }
}

for my $key (keys %auths) {
  my $entry =  "$key;";
  $entry .= "$auths{$key}{'earliest'};";
  $entry .= "$auths{$key}{'latest'};";
  $entry .= "$auths{$key}{'e_commit'};";
  $entry .= "$auths{$key}{'l_commit'};";

  print B $entry . "\n";
}

close A;
close B;

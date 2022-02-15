use strict;
use warnings;

my %auths = ();

my $file = 'timeline.sorted.out';
#my $file = 'test.out';
my $output = 'timeline.all.out';

open A, $file or die $!;
open B, '>>', $output or die $!;

while(<A>) {
  chop();

  my @contents = split(/;/);
  my $auth = $contents[0];
  my $earliest = $contents[1];
  my $latest = $contents[2];
  my $e_commit = $contents[3];
  my $l_commit = $contents[4];

  if (not exists $auths{$auth}) {

    if(%auths) {
      for my $key (keys %auths) {
        my $entry =  "$key;";
        $entry .= "$auths{$key}{'earliest'};";
        $entry .= "$auths{$key}{'latest'};";
        $entry .= "$auths{$key}{'e_commit'};";
        $entry .= "$auths{$key}{'l_commit'}";

        print B $entry . "\n";
      }
      %auths = ();
    }

    $auths{$auth}{"earliest"} = $earliest;
    $auths{$auth}{"e_commit"} = $e_commit;
    $auths{$auth}{"latest"} = $latest;
    $auths{$auth}{"l_commit"} = $l_commit;
  } 
  elsif ($auths{$auth}{"earliest"} gt $earliest) {
    $auths{$auth}{"earliest"} = $earliest;
    $auths{$auth}{"e_commit"} = $e_commit;
  }
  elsif ($auths{$auth}{"earliest"} gt $latest) {
    $auths{$auth}{"earliest"} = $latest;
    $auths{$auth}{"e_commit"} = $l_commit;
  }
  elsif ($auths{$auth}{"latest"} lt $earliest) { 
    $auths{$auth}{"latest"} = $earliest;
    $auths{$auth}{"l_commit"} = $e_commit;
  }
  elsif ($auths{$auth}{"latest"} lt $latest) { 
    $auths{$auth}{"latest"} = $latest;
    $auths{$auth}{"l_commit"} = $l_commit;
  }
}

if(%auths) {
  for my $key (keys %auths) {
    my $entry =  "$key;";
    $entry .= "$auths{$key}{'earliest'};";
    $entry .= "$auths{$key}{'latest'};";
    $entry .= "$auths{$key}{'e_commit'};";
    $entry .= "$auths{$key}{'l_commit'}";

    print B $entry . "\n";
  }
  %auths = ();
}

close A;
close B;

use strict;
use warnings;

my %tmp = ();

while(<>) {
  chomp $_;
  my @line = split(/;/, $_);
  my $commit = $line[2];

  my $output = `echo $commit | ~/lookup/getValues c2f 2> /dev/null`;
  my @files = split(/;/, $output);

  my %e = ();

  for my $file (@files) { ext ($file, \%e) }
  my $languages = "";
  for my $i (keys %e) {
    if($i ne "other") {
      $languages .= "$i,";
    }
  }
  if($languages ne "") {
    chop($languages);
    print $_ . ';' . $languages;
    print "\n";
  }
}


sub ext {
  my ($f, $stats) = @_;
  if( $f =~ m/(\.java$|\.iml|\.jar|\.class|\.dpj|\.xrb)$/ ) {$stats->{'Java'}++;}
  elsif( $f =~ m/\.(js|iced|liticed|iced.md|coffee|litcoffee|coffee.md|cs|ls|es6|jsx|sjs|co|eg|json|json.ls|json5)$/ ) {$stats->{'JavaScript'}++;}
  elsif( $f =~ m/\.(py|py3|pyx|pyo|pyw|pyc|whl)$/ ) {$stats->{'Python'}++;}
  elsif( $f =~ m/\.CPP$|\.CXX$|\.cpp$|\.[Cch]$|\.hh$|\.cc$|\.cxx$|\.hpp$|\.hxx$|\.Hxx$|\.HXX$|\.C$|\.c$|\.h$|\.H$/ ) { $stats->{'C/C++'}++; }
  elsif( $f =~ m/\.cs$/ )    {$stats->{'C#'}++;}
  elsif( $f =~ m/\.php$/ )     {$stats->{'PHP'}++;}
  elsif( $f =~ m/\.(rb|erb|gem|gemspec)$/ )    {$stats->{'Ruby'}++;  }
  elsif( $f =~ m/\.go$/ )      {$stats->{'Go'}++;}
  elsif( $f =~ m/\.ipy$/ ) {$stats->{'ipy'}++;}
  elsif( $f =~ m/\.swift$/ )   {$stats->{'Swift'}++;}
  elsif( $f =~ m/\.scala$/ )   {$stats->{'Scala'}++;}
  elsif( $f =~ m/\.(kt|kts|ktm)$/ ) {$stats->{'Kotlin'}++;}
  elsif( $f =~ m/\.(ts|tsx)$/ ) {$stats->{'TypeScript'}++;}
  elsif( $f =~ m/\.dart$/ ) {$stats->{'Dart'}++;}
  elsif( $f =~ m/\.(rs|rlib|rst)$/ )   {$stats->{'Rust'}++;}
  elsif( $f =~ m'./*(\.Rd|\.[Rr]|\.Rprofile|\.Rdata|\.Rhistory|\.Rproj|^NAMESPACE|^DESCRIPTION|/NAMESPACE|/DESCRIPTION)$' )    {$stats->{'R'}++;}
  elsif( $f =~ m/(\.perl|\.pod|\.pl|\.PL|\.pm)$/ ){ $stats->{'Perl'}++; }
  elsif( $f =~ m/\.(f[hi]|[fF]|[fF]77|[fF]9[0-9]|fortran|forth)$/ )    {$stats->{'Fortran'}++;}
  elsif( $f =~ m/\.ad[abs]$/ ) {$stats->{'Ada'}++;}
  elsif( $f =~ m/\.erl$/ )     {$stats->{'Erlang'}++;}
  elsif( $f =~ m/\.lua$/ )     {$stats->{'Lua'}++;}
  elsif( $f =~ m/\.(sql|sqllite|sqllite3|mysql)$/ )    {$stats->{'Sql'}++;}
  elsif( $f =~ m/\.(el|lisp|elc)$/ )   {$stats->{'Lisp'}++;}
  elsif( $f =~ m/\.(fs|fsi|ml|mli|hs|lhs|sml|v)$/ )    {$stats->{'fml'}++;}
  elsif( $f =~ m/\.jl$/ )      {$stats->{'Julia'}++;}   
  elsif( $f =~ m/\.(COB|CBL|PCO|FD|SEL|CPY|cob|cbl|pco|fd|sel|cpy)$/ ) {$stats->{'Cobol'}++;}
  elsif( $f =~ m/\.(cljs|cljc|clj)$/ ) {$stats->{'Clojure'}++;}
  elsif( $f =~ m/\.(aug|mli|ml|aug)$/ ) {$stats->{'OCaml'}++;}
  elsif( $f =~ m/\.(bas|bb|bi|pb)$/ ) {$stats->{'Basic'}++;}
  else {$stats->{'other'}++};
}

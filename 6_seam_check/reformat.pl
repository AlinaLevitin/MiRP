#!/usr/bin/perl
use strict;

my $notprinted = 1;
my @head;
while(<STDIN>) {
    chomp;
    my @a = split;
    if (  /_rln(\w+)/ ) {
        push @head , $1
    }
    elsif ( $#a > 3 && /\w+/ ) {
        if ( $notprinted ) {
            print join( "\t", @head ) . "\n" ;
            $notprinted = 1;
        }
        print $_ . "\n";
    }
}
#
#This Perl script appears to process input from STDIN (standard input), likely structured data. Here's a breakdown of
#what it does:
#
#1. It begins with a shebang line (`#!/usr/bin/perl`) indicating that this script should be interpreted by Perl.
#
#2. It enables strict mode, which enforces more rigorous syntax and variable declaration rules, helping to catch errors.
#
#3. It initializes a variable `$notprinted` to 1 and an array `@head`.
#
#4. It enters a `while` loop that reads input line by line from STDIN (`<STDIN>`).
#
#5. Within the loop:
#   - It removes the newline character from the input line using `chomp`.
#   - It splits the input line into an array `@a` using whitespace as the delimiter.
#   - It checks if the line matches a pattern `/_rln(\w+)/`. If it does, it extracts the capture group (`$1`) and pushes
#   it onto the `@head` array.
#   - If the line doesn't match the first pattern (`elsif ( $#a > 3 && /\w+/ )`), and if the number of elements in `@a`
#   is greater than 3 and the line contains at least one word character (`\w+`), it executes the following:
#      - If `$notprinted` is true (equal to 1), it prints the elements of `@head` joined by tabs, followed by a newline.
#      - It then prints the current line.
#      - Sets `$notprinted` back to 1.
#
#This script appears to be designed to process structured input, likely with column headers marked by lines matching the
#pattern `/_rln(\w+)/`, and then printing the lines of data, with the first line being the column headers. However,
#it seems there might be a logical error in the script. The variable `$notprinted` is initialized to 1 but never set to
#0, so the condition `$notprinted` is always true, and the column headers are printed before every data line.

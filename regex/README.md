# regular expression matcher


Regular expression matcher that can match patterns with a-z, "." (for any single char), and "*" (for any string)


Example

match(a, a) = true;

match(a, b) = false;

match(c, .) = true

match(de, *) = true;

match(abc, c*) = false;

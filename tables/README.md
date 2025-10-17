# Tables in this folder

## Tables that also appear in the paper

* Table 6.10 (`maximal_promise_useful_k3.txt`)
* Table 6.11 (`minimal_promise_useless_k3.txt`)
* Table 6.12 (`maximal_promise_useful_k4.txt`)
* Table 6.13 (`minimal_promise_useless_k4.txt`)
* Table 6.14 (`maximal_promise_useful_k5.txt`)

* Table B.1 (`maximal_tractable_k5.txt`)
* Table B.2 (`minimal_unknown_k5.txt`)
* Table B.3 (`maximal_unknown_k5.txt`)
* Table B.4 (`minimal_promise_unknown_k5.txt`)
* Table B.5 (`maximal_promise_unknown_k5.txt`)

The tables given here as .txt files only contain the predicates.
The predicates are listed in the same order here as in the paper.

## Tables that do not appear in the paper

The following tables were left out of the paper for the sake of brevity.

* `maximal_tractable_k2.txt`
* `maximal_tractable_k3.txt`
* `maximal_tractable_k4.txt`
* `minimal_hard_k3.txt`
* `minimal_hard_k4.txt`
* `minimal_hard_k5.txt`

* `maximal_promise_useful_k2.txt`
* `minimal_promise_useless_k5.txt`

## Empty tables
Some of the files are empty (for example because there are no unknowns for k <= 4). They are

* `minimal_hard_k2.txt`
* `maximal_unknown_k2.txt`
* `maximal_unknown_k3.txt`
* `maximal_unknown_k4.txt`
* `minimal_unknown_k2.txt`
* `minimal_unknown_k3.txt`
* `minimal_unknown_k4.txt`

* `minimal_promise_useless_k2.txt`
* `maximal_promise_unknown_k2.txt`
* `maximal_promise_unknown_k3.txt`
* `maximal_promise_unknown_k4.txt`
* `minimal_promise_unknown_k2.txt`
* `minimal_promise_unknown_k3.txt`
* `minimal_promise_unknown_k4.txt`

# File format used for .txt files
The first line contains two numbers, n and k,
where n is the number of predicates and k is the arity of the predicates.

Then there are 2n more lines.

The 2i-th line contains an integer m_i.
The (2i+1)-th line contains m_i, space seperated, strings of length k consisting of the characters 0, 1 or \*,
where \* deontes a wildcard character.

A bitstring in {0,1}^k is contained in the i-th predicate iff
that bitstring matches one of the m_i strings.
In most cases there will be no wildcards. Then the i-th predicate
contains precisely the m_i bitstrings given on the (2i+1)-th line.

See `parse_tables.py` for an example of how to parse these files.

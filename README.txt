Competition organised by Google in 2020. The objective is to answer a given
problem, on the theme of data processing.
The script is made in Python V3. No external library is needed.
The results are calculated and displayed directly in the terminal. The files 
to be processed are [here](Output).

## Issue
Books allow us to discover fantasy worlds and better understand the world we 
live in.
They enable us to learn about everything from photography to compilers… and of 
course a good book is a great way to relax!

Last 15 years, Google Books has collected digital copies of 40 million books 
in more than 400 languages.

In this competition problem, we will explore the challenges of seing up a 
scanning process for millions of books stored i n l ibraries around the world 
and having them scanned at a scanning facility.

### Objectives ✔
Given a description of libraries and books available, plan which books to scan 
from which library to maximize the total score of all scanned books, taking 
into account that each library needs to be signed up before it can ship books.

### Score Calculation
Your score is the sum of the scores of all books that are scanned within D days. 
Note that if the same book is shipped from multiple libraries, the solution will
be accepted but the score for the book will be awarded only once.

## Solution
### Principle
It is important to have read the instructions for the competition
(hashcode_2020_online_qualification_round.pdf) beforehand, to understand 
the rest.

The ratio of library, number of days borrowed / total book score, is calculated.
This allows us to sort them.

We start with the library with the highest ratio, on day 0, we add the signup 
process time.
We start to return the books, starting with the books with the highest score.
And those that we still have books or days left to return.

Once this library is finished, we recalculate all the ratios of all the 
librarys. This makes it possible to delete the books that have already been 
rendered. This way we always treat the library that yields the most points.

We do the same treatment as for the first library, but the day after the signup
process of the previous library. 
We continue in this way while we still have time to do the signup process of 
at least one library.

### Score
This is calculated directly by the script.

File                         | Number of libairys | Number of books | Number of days | Score      | Time 
---------------------------- | ------------------ | --------------- | -------------- | ---------- | -------------
a_example.txt                | 6                  | 2               | 7              | 21         | 00h 00min 00s
b_read_on.txt                | 100 000            | 100             | 1 000          | 5 822 900  | 00h 03min 09s
c_incunabula.txt             | 100 000            | 10 000          | 100 000        | 5 689 822  | 00h 02min 39s
d_tough_choices.txt          | 78 600             | 30 000          | 30 001         | 5 028 010  | 00h 24min 39s
e_so_many_books.txt          | 100 000            | 1 000           | 200            | 4 593 379  | 00h 02min 43s
f_libraries_of_the_world.txt | 100 000            | 1 000           | 700            | 5 208 176  | 00h 01min 25s
Total                        | 478 606            | 42 102          | 131 908        | 26 342 308 | 00h 34min 38s

The calculated score is confirmed by the Judge System of the HashCode.

### Limits ⚠
- No unit test
- The comments of the code are in French 🇫🇷
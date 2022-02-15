from oscar import Author

with open('authors.sample.out') as f:
  for line in f:
    commits = tuple(Author(line).commits);
    print(commits)

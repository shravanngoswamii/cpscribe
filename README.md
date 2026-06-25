# cpscribe

Generate structured blog posts for Codeforces solutions.

## Install

```sh
pipx install cpscribe
```

## Setup

```sh
cpscribe init
```

This creates `~/.config/cpscribe/config` with your blog root and author name.
You can also set `CPSCRIBE_BLOG_ROOT` and `CPSCRIBE_AUTHOR` as environment variables.

## Usage

```sh
# from a URL
cpscribe post https://codeforces.com/contest/1903/problem/B

# from a .cpp file with a URL in a comment
cpscribe post B.cpp

# with an explicit solution file
cpscribe post https://codeforces.com/contest/1903/problem/B B.cpp
```

The generated post includes the full problem statement, sample I/O, and structured
sections for your approach, complexity, solution, and takeaways.

## Update

```sh
pipx upgrade cpscribe
```

## License

MIT

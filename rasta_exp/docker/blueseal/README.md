# Blueseal

- [source](https://github.com/ub-rms/blueseal)
- [paper](https://dl.acm.org/doi/10.1145/2642937.2643018)
- language: Java7
- Build: Ant
- number of years without at least 1 commit since first commit: 7
- License: None

## Notes

Troubles on laptop:

Build:

```
docker build --ulimit nofile=65536:65536 .
```

Run 

```
docker run --ulimit nofile=65536:65536 -it -v ... 
```


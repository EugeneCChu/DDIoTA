---
layout: default
---

## Progress

### 2019/10/26

**First Phase Complete**
1. Front-end program can extract sentence from speech with high accuracy
2. Back-end analysis can extract `DEVICE NOUN` from text 
3. Currently no parameters or specific actions can be determined

**TODO**
1. Continue onto second phase

```markdown
Python speech to text → SpaCy Part-Of-Speech tagger
```

### 2019/10/31

**Second Phase -- 50%**
1. Added *Syntatic Dependency Parsing* allowing creation of parse trees
2. Separation of `DEVICE NOUN`, `PARAMETER NOUN` and their corresponding `VERB`s

**TODO**
1. Rule-based matching to account for inaccuracy in parse trees
2. Word embeddings(BERT/Flair) for synonyms


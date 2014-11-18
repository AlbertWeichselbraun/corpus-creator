Enables researchers to publish text corpora without violating the publisher's text copyrights.

Corpus diff computes a 'cdiff' file between an input HTML file and a list of sentences which have been extracted from the HTML file. 
Researchers can publish these 'cdiff' files which can then be used to create the corpus which they have used for their evaluations, provided that the input resource is still available.

## Workflow

### Generate corpus diff

* convert the input document to text
* obtain a list of unique text tokens within the document
* select the first, the last and "n-2" random anchors within the document
* compare the input document with the output document and compute for every sentence
  1. the relative position to all "n" anchors, 
  2. its first three letters
  3. its last three letters
  4. the sentence length
  5. the first 6 bytes of the sentence's md5sum


### Apply corpus diff

* convert the input document to text
* for every sentence:
  1. compute its start position based on the anchors
  2. verify the sentence length, prefixes and suffixes.
  3. extract the sentence
* conflict handling:
  1. based on the prefixes and suffixes

### Command line client
```sh
usage: corpus-creator.py [-h] [--html-resource HTML_RESOURCE]
                         [--txt-resource TXT_RESOURCE] [--output OUTPUT]
                         [--working-directory WORKING_DIRECTORY] [--url URL]
                         cdiff
```

**Example Calls**

* create a cdiff based on an HTML and text resource
```sh
./corpus-creator.py --html-resource Chur.html --txt-resource Chur.txt Chur.cdiff
```

* restore the text based on the *cdiff* file:
```sh
./corpus-creator.py chur.cdiff
```


### Example output and format description

```
http://en.wikipedia.org/wiki/Chur
Wikipedia,:13 Terracina:1005 seat:2285 sites;:8589 Planta,:19306 religion:19751 October:24765
> -19752 -19307 -1006 -14 -8590 -2286 -24766 Chu on. 110 cc269d
> -18539 -18094 207 1199 -7377 -1073 -23553 The nd. 109 27cc51
> -15181 -14736 3565 4557 -4019 2285 -20195 Aft 03. 85 837e25
> -19752 -19307 -1006 -14 -8590 -2286 -24766 The de. 132 2c7d93
> -14958 -14513 3788 4780 -3796 2508 -19972 Whe al. 72 18a464
> -12171 -11726 6575 7567 -1009 5295 -17185 The in. 200 4a19b4
> -11717 -11272 7029 8021 -555 5749 -16731 The ur. 167 aadf95
> -19752 -19307 -1006 -14 -8590 -2286 -24766 The ol. 181 2d2d77
> -4753 -4308 13993 14985 6409 12713 -9767 The B). 120 a04492
> -4632 -4187 14114 15106 6530 12834 -9646 Whi hn. 267 cff962
```

**Format description**

```
at1:at1_pos| [at2:at2_pos, ...atn:atn_pos]
> s1_at1_pos [s1_at2_pos, ... s1_atn_pos] s1_start_let s1_end_let s1_len s1_checksum
> s2_at1_pos [s2_at2_pos, ... s2_atn_pos] s2_start_let s2_end_let s2_len s2_checksum
```

1. `at1` ... anchor term 1
1. `at1_pos` ... start index of anchor term 1
1. `s1_at1_pos` ... start index of sentence 1 relative to anchor term 1
1. `s2_at1_pos` ... start index of sentence 2 relative to anchor term 1
1. `s1_start_let` ... the first three letters of sentence 1
1. `s1_end_let` ... the last three letters of sentence 1
1. `s1_len` ... the length of sentence 1
1. `s1_checksum` ... the last 24 bit of the md5 hash of sentence 

## Future work:

* try to obtain open-archive links for documents

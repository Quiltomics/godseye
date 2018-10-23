<div align="center">

# godseye

<img src="https://user-images.githubusercontent.com/9893806/40345517-55dc748c-5d4e-11e8-821c-7a12ad772000.png" height="400" width="400">

##### Monitor biomedical trends visually across ALL of PubMed + bioRxiv

</div>

## About

### Introduction
Bioinformatics is one of the [fastest growing interdisciplinary fields](http://science.sciencemag.org/content/344/6189/1303). As new technologies emerge, new types of data come into the spotlight, thereby creating the need for novel computational approaches and methodologies that can successfully deal with those new data. As a result, the interest of the community for specific areas often shifts dramatically over a short amount of time. Here we present a text mining approach to systematically identify trending topics in Bioinformatics over time and space, as embodied in journal articles' abstracts and titles.

Using keyword prominence and an efficient temporal segmentation algorithm, our method highlights trending topics in the bioinformatics literature, and can be helpful in predicting the ever-changing demands of the bioinformatics job market.

### Data Sources
We quilted together the NCBI MEDLINE®/PubMed® database and bioRxiv® database to extract all titles, abstracts, and author affiliations of all published papers and preprints, respectively.

### Impact
By including bioRxiv, `godseye` can monitor the pulse of the biological research community with a delay of several days at most, which is the average time it takes for a preprint to be publicly displayed on bioRxiv upon submission.  In contrast, PubMed's delay is at least 3-18 months, which is often the time range of the lengthy peer-review cycle.  Once a preprint is published in a peer-reviewed journal and thereby available on PubMed, `godseye` delegates to the PubMed resource for extracting information from the abstract/title (since these are often updated relative to the bioRxiv version of the paper).  

### Algorithms
#### Keyword prominence in a time range
We define the prominence of a keyword _w_ as the fraction of journal abstracts in a given time range that contain the keyword _w_. An arbitrary parameter _α_ is then chosen to filter out keywords whose prominence is _<_ _α_.

#### Temporal segmentation of the journal titles and abstracts
The main idea is to optimally segment the yearly data into smaller contiguous time ranges, in a way that maximizes the overlap of prominent keywords within the resulting temporal segments. The algorithm uses dynamic programming to efficiently compute an optimal segmentation, and takes as input the keyword frequency per year and the desired number of temporal segments n. For more information on the original implementation of the algorithm, see [Siy et al.](https://dl.acm.org/citation.cfm?id=1379054)  The algorithm returns the optimal segments and a list of prominent keywords in each segment.

## Future plans

- [x] Modularize Python code with OOP methods
- [ ] Analyze PDF/HTML contents of a PubMed or bioRxiv paper, not just its abstract, title, and author affiliations.  For this task, consider integrating existing tools like [fulltext](https://github.com/ropensci/fulltext), [pdftools](https://github.com/ropensci/pdftools), and [pubcrawl](https://github.com/hrbrmstr/pubcrawl)
- [ ] Implement dynamic programming algorithm to achieve optimal temporal segmentation.  But also re-consider other algorithm choices (besides for temporal segmentation) because perhaps there are other more suitable (optimal) alternatives
- [ ] Expand `godseye` into ML territory with [snorkel](http://mobilize.stanford.edu/events/snorkelworkshop2018/)
- [ ] Implement graph database to understand the relation between any set of keywords over a time period or geographical region (e.g., the spatial and temporal evolution of keyword co-occurrences)

## Contact
You are welcome to:

* submit suggestions and bug-reports at: <https://github.com/Quiltomics/godseye/issues>
* send a pull request on: <https://github.com/Quiltomics/godseye>
* compose an e-mail to: <bohdan@stanford.edu>

## Code of conduct
Please note that this project is released with a [Contributor Code of Conduct](CONDUCT.md). By participating in this project you agree to abide by its terms.

## Contributors (alphabetical by last name)
* Nanda Kishore Adapa
* [Parvathi Chundi, Ph.D.](https://www.unomaha.edu/college-of-information-science-and-technology/about/faculty-staff/parvathi-chundi.php)
* [Dario Ghersi, M.D. Ph.D.](https://www.unomaha.edu/college-of-information-science-and-technology/about/faculty-staff/dario-ghersi.php)
* [Bohdan Khomtchouk, Ph.D.](https://github.com/Bohdan-Khomtchouk)
* [Kasra A. Vand](https://github.com/kasramvd)

## Attribution
This work is a hard fork of [biotrends](https://github.com/thecodingdoc/biotrends).  It is an academic partnership between Drs. Ghersi and Khomtchouk at UNO and Stanford, respectively.

## Citation
Coming soon!

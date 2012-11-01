World Attention Map
===================

This is a simple script to turn some data about world media attention by country into a 
black and white heatmap. 

Installation
------------

* Pyton2.6 or greater
* Install [BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/)
* Download and install [incf.countryutils 1.0](http://pypi.python.org/pypi/incf.countryutils)

Use
---

The input HTML data is in the `gnews20101001.html` file.  Run the `html-to-css.py` 
script to generate a `country_colors.css` file.  Paste that CSS into `<style>` block 
of the `BlankMap-World6.svg` file.  Open that file with a web browser to render it.

Sources
-------

* [Wikipedia World SVG Map](http://en.wikipedia.org/wiki/File:BlankMap-World6.svg)
* [Berkman Center World Attention Data](http://dawn.law.harvard.edu:8080/results/20101001/gnews20101001.html)

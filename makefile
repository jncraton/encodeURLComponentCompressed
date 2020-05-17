all: freqs

freqs: freqs.py ucomp.js
	python3 freqs.py
	nodejs ucomp.js
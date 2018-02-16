Authors:
	Lorena Dieste Maroñas
	Sergio Sancho Sanz

For executing both searcher and indexer, files must be saved as follows:
	
	corpora (same structure as in Faitic)
		cf
			...
		moocs
			...

	indices
		moocs_indexer.dat
		cf_indexer.dat

	searcher.py
	indexer.py


In order to know how to invoke each file, you can type:
	
	python indexer.py -h
	python searcher.py -h


Both indices have been generated already.
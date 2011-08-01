#!/usr/bin/env python
import re
import urllib
from BeautifulSoup import BeautifulSoup

base_url = "http://ci.apps-system.com/job"

def get_build_page(build):
	f = urllib.urlopen("%s/%s/" % (base_url, build))
	page = f.read()
	f.close()
	return BeautifulSoup(page)

def get_coverage(page):
	return page.findAll(text=re.compile("Cobertura Coverage"))[0]

def get_test_results(page):
	return page.findAll(text=re.compile("Test Result:"))[0]

def get_cobertura_graph(build):
	return "%s/%s/cobertura/graph" % (base_url, build)
	
def get_test_graph(build):
	return "%s/%s/test/trend" % (base_url, build)
	
def get_violations_graph(build):
	return "%s/%s/violations/graph" % (base_url, build)

def get_cpd_graph(build):
	return "%s/%s/violations/graph?type=cpd" % (base_url, build)

def get_pylint_graph(build):
	return "%s/%s/violations/graph?type=pylint" % (base_url, build)

if __name__ == '__main__':
	vector_build = 'Vector_Build'
	vector_page = get_build_page(vector_build)
	print get_coverage(vector_page)
	print get_cobertura_graph(vector_build)
	print get_test_results(vector_page)
	print get_test_graph(vector_build)


	vector_analysis_build = "Vector_Analysis"
	print get_violations_graph(vector_analysis_build)	
	print get_cpd_graph(vector_analysis_build)	
	print get_pylint_graph(vector_analysis_build)	
	

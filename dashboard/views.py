
from django.views.generic import TemplateView
from BeautifulSoup import BeautifulSoup
import re
import urllib
import time

ci_url = "http://ci.apps-system.com/"
base_url = "%s/job" % ci_url

builds = [
    'django-admin-ext',
    'django-dynamic-rules',
    'django-dynamic-validation',
    'django-forms-ext',
    'django-dynamic-manipulation',
    'django-wizard',
    'django-pretty-times',
    'django-response-helpers',
    'django-attachments',
]

class Status(TemplateView):
    template_name = 'dashboard/status.html'

    def get_context_data(self, **kwargs):
        f = urllib.urlopen(ci_url)
        data = f.read()
        f.close()
        page = BeautifulSoup(data)

        status_table = page.findAll(**{'id': 'projectstatus'})[0]
        statuses = []
        for cell in status_table.findAll('tr')[1:]:
            status_icon = cell.find('img', **{'class': 'icon32x32'})
            if status_icon:
                statuses.append(dict(status_icon.attrs)['alt'])

        ss = [s not in ('Success', 'Disabled', 'In progress', 'Pending') for s in statuses]
        fail = any(ss)
        if fail:
            for i in range(20):
                print "\a"
                time.sleep(.2)

        return {'success': not fail}

class Index(TemplateView):
    template_name = 'dashboard/index.html'
    current_build = -1

    def get_context_data(self, **kwargs):
        Index.current_build += 1
        if Index.current_build >= len(builds):
            Index.current_build = 0

        build = builds[Index.current_build]
        return {
            'params': kwargs,
            'status':self.get_status(),
            'build': build,
            'test_section_title':'Tests',
            'test_section_content':self.get_test_graph(build),
            'coverage_section_title':'Coverage',
            'coverage_section_content':self.get_cobertura_graph(build),
            'violations_section_title':'Violations',
            'violations_section_content':self.get_violations_graph(build),
            'pylint_section_title':'Pylint',
            'pylint_section_content':self.get_pylint_graph(build),
            'cpd_section_title':'CPD',
            'cpd_section_content':self.get_cpd_graph(build),
            'pep8_section_title':'Pep8',
            'pep8_section_content':self.get_pep8_graph(build),
        }

    def get_status(self):
        page = get_build_page(builds[Index.current_build] + "/lastBuild")
        status = get_status(page)
        return status.replace(" ", '')

    def get_test_graph(self, build):
        return "%s/%s/test/trend" % (base_url, build)

    def get_cobertura_graph(self, build):
        return "%s/%s/cobertura/graph" % (base_url, build)


    def get_violations_graph(self, build):
        return "%s/%s/violations/graph" % (base_url, build)

    def get_pylint_graph(self, build):
        return "%s/%s/violations/graph?type=pylint" % (base_url, build)

    def get_cpd_graph(self, build):
        return "%s/%s/violations/graph?type=cpd" % (base_url, build)

    def get_pep8_graph(self, build):
        return "%s/%s/violations/graph?type=pep8" % (base_url, build)

def get_build_page(build):
    f = urllib.urlopen("%s/%s/" % (base_url, build))
    page = f.read()
    f.close()
    return BeautifulSoup(page)

def get_coverage(page):
    return page.findAll(text=re.compile("Cobertura Coverage"))[0]

def get_test_results(page):
    return page.findAll(text=re.compile("Test Result:"))[0]

def get_status(page):
    return page.findAll(src="buildStatus")[0]['alt']


#def get_violation_results(violation_type, page):
#    violation = page.find('a', {'href':'#' + violation_type})
#    violation_count = violation.parent.nextSibling
#    return (violation_count.text, violation_count.nextSibling.text)

#def get_image_html(src):
#    return r"<img src='%s' />" % src

#def get_section(title, content):
#    return """
#        <div class="column">
#            <div class="section">
#                <h2>%s</h2>
#                %s
#            </div>
#        </div>
#    """ % (title, content)
#
#def build_stats(build):
#
#    #build, status
#
##    print get_section("CPD", get_image_html(get_cpd_graph(build)))
##    print get_section("Pep8", get_image_html(get_pep8_graph(build)))
##    print """<div style="clear:both;" />"""
#
#
#def x():
#    for build in builds:
#        build_stats(build)

#!/usr/bin/env python

"""
  This file is part of FIRS Industry Set for OpenTTD.
  FIRS is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, version 2.
  FIRS is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  See the GNU General Public License for more details. You should have received a copy of the GNU General Public License along with FIRS. If not, see <http://www.gnu.org/licenses/>.
"""
print "[PYTHON] render docs"

import codecs # used for writing files - more unicode friendly than standard open() module

import shutil
import sys
import os.path
currentdir = os.curdir

docs_src = os.path.join(currentdir, 'docs_src')
docs_output_path = os.path.join(currentdir, 'docs')
if os.path.exists(docs_output_path):
    shutil.rmtree(docs_output_path)
os.mkdir(docs_output_path)

shutil.copy(os.path.join(docs_src,'index.html'), docs_output_path)

static_dir_src = os.path.join(currentdir, 'docs_src', 'html', 'static')
static_dir_dst = os.path.join(docs_output_path, 'html', 'static')
shutil.copytree(static_dir_src, static_dir_dst)

from chameleon import PageTemplateLoader # chameleon used in most template cases
# setup the places we look for templates
docs_templates = PageTemplateLoader(os.path.join(currentdir, 'docs_src'), format='text')

import global_constants as global_constants
import utils as utils

# get args passed by makefile
repo_vars = utils.get_repo_vars(sys)

# get the strings from base lang file so they can be used in docs
base_lang_strings = utils.parse_base_lang()

metadata = {}
metadata['dev_thread_url'] = 'http://www.tt-forums.net/viewtopic.php?t=41607'
metadata['repo_url'] = 'http://dev.openttdcoop.org/projects/firs/repository'
metadata['issue_tracker'] = 'http://dev.openttdcoop.org/projects/firs/repository'

import firs
from cargos import registered_cargos
from industries import registered_industries
# default sort for docs is by id
registered_cargos = sorted(registered_cargos, key=lambda registered_cargos: registered_cargos.id)
registered_industries = sorted(registered_industries, key=lambda registered_industries: registered_industries.id)

class DocHelper(object):
    # dirty class to help do some doc formatting
    def get_economy_name(self, economy):
        string_id = "STR_PARAM_VALUE_ECONOMIES_" + economy
        name_string = base_lang_strings.get(string_id, 'NO_NAME ' + economy)
        return name_string.split(' Economy')[0] # name strings contain 'economy', I don't want that in docs

    def get_cargo_name(self, cargo):
        # cargos don't store the name directly as a python attr, but in lang - so look it up in base_lang using string id
        name = cargo.type_name
        string_id = utils.unwrap_nml_string_declaration(name)
        return base_lang_strings.get(string_id, 'NO NAME ' + str(name) + ' ' + cargo.id)

    def get_industry_name(self, industry, economy=None):
        # industries don't store the name directly as a python attr, but in lang - so look it up in base_lang using string id
        name = industry.get_property('name', economy)
        string_id = utils.unwrap_nml_string_declaration(name)
        return base_lang_strings.get(string_id, 'NO NAME ' + str(name) + ' ' + industry.id)

    def get_industry_all_name_strings(self, industry):
        # names can vary in each economy
        result = []
        for economy in economy_schemas:
            name = industry.get_property('name', economy)
            result.append(utils.unwrap_nml_string_declaration(name))
        return set(result)

    def get_industry_all_names(self, industry):
        # names can vary in each economy
        result = []
        for name_string in self.get_industry_all_name_strings(industry):
            result.append(base_lang_strings.get(name_string, 'NO NAME ' + name_string + ' ' + industry.id))
        return set(result)

    def get_economies_sorted_by_name(self):
        return sorted(global_constants.economies, key=lambda economy: self.get_economy_name(economy))

    def get_registered_cargo_sorted_by_name(self):
        # cargos don't store the name as a python attr, but we often need to iterate over their names in A-Z order
        result = dict((self.get_cargo_name(cargo), cargo) for cargo in registered_cargos)
        return sorted(result.items())

    def get_registered_industries_sorted_by_name(self):
        # industries don't store the name as a python attr, but we often need to iterate over their names in A-Z order
        result = dict((self.get_industry_name(industry), industry) for industry in registered_industries)
        return sorted(result.items())

    def get_economy_extra_info(self, economy):
        return base_lang_strings.get('ECONOMY_INFO_' + economy, '')

    def get_cargo_extra_info(self, cargo):
        return base_lang_strings.get('CARGO_INFO_' + cargo.id.upper(), '')

    def get_industry_extra_info(self, industry):
        return base_lang_strings.get('INDUSTRY_INFO_' + industry.id.upper(), '')

    def industry_find_industries_active_in_economy_for_cargo(self, cargo, economy, accept_or_produce):
        result = []
        if cargo in economy_schemas[economy]['enabled_cargos']:
            for industry in economy_schemas[economy]['enabled_industries']:
                    for cargo_label in industry.get_property(accept_or_produce, economy):
                        if cargo.cargo_label[1:-1] == cargo_label:
                            result.append(industry)
        return set(result)

    def cargo_unique_industry_combinations(self, cargo):
        result = {}
        for economy in self.get_economies_sorted_by_name():
            economy_industries = []
            accepted_by = self.industry_find_industries_active_in_economy_for_cargo(cargo, economy, 'accept_cargo_types')
            produced_by = self.industry_find_industries_active_in_economy_for_cargo(cargo, economy, 'prod_cargo_types')
            for industry in accepted_by:
                economy_industries.append(industry)
            for industry in produced_by:
                economy_industries.append(industry)
            if len(economy_industries) > 0:
                industry_key = tuple(sorted(economy_industries))
                result.setdefault(industry_key, {'accepted_by': accepted_by, 'produced_by': produced_by})
                result[industry_key].setdefault('economies',[]).append(economy)
                 # convenient to have items sorted
                result[industry_key]['economies'] = sorted(result[industry_key]['economies'], key=lambda economy: self.get_economy_name(economy))
        # return a list, sorted by economies (only need first economy entry in each list of economies)
        return sorted(result.values(), key = lambda combo: self.get_economy_name(combo['economies'][0]))


    def industry_find_cargos_active_in_economy_for_industry(self, industry, economy, accept_or_produce):
        result = []
        if industry in economy_schemas[economy]['enabled_industries']:
            for cargo_label in industry.get_property(accept_or_produce, economy):
                for cargo in economy_schemas[economy]['enabled_cargos']:
                    if cargo_label == cargo.cargo_label[1:-1]:
                        result.append(cargo)
        return set(result)

    def industry_unique_cargo_combinations(self, industry):
        result = {}
        for economy in self.get_economies_sorted_by_name():
            economy_cargos = []
            accept_cargo_types = self.industry_find_cargos_active_in_economy_for_industry(industry, economy, 'accept_cargo_types')
            prod_cargo_types = self.industry_find_cargos_active_in_economy_for_industry(industry, economy, 'prod_cargo_types')
            for cargo in accept_cargo_types:
                economy_cargos.append(cargo)
            for cargo in prod_cargo_types:
                economy_cargos.append(cargo)
            if len(economy_cargos) > 0:
                cargo_key = tuple(sorted(economy_cargos))
                result.setdefault(cargo_key, {'accept_cargo_types': accept_cargo_types, 'prod_cargo_types': prod_cargo_types})
                result[cargo_key].setdefault('economies',[]).append(economy)
                 # convenient to have items sorted
                result[cargo_key]['economies'] = sorted(result[cargo_key]['economies'], key=lambda economy: self.get_economy_name(economy))
        # return a list, sorted by economies (only need first economy entry in each list of economies)
        return sorted(result.values(), key = lambda combo: self.get_economy_name(combo['economies'][0]))


    def get_active_nav(self, doc_name, nav_link):
        return ('','active')[doc_name == nav_link]


def render_docs(doc_list, file_type):
    for doc_name in doc_list:
        template = docs_templates[doc_name + '.pt'] # .pt is the conventional extension for chameleon page templates
        doc = template(registered_cargos=registered_cargos, registered_industries=registered_industries,
                              economy_schemas=economy_schemas, global_constants=global_constants, repo_vars=repo_vars,
                              metadata=metadata, utils=utils, doc_helper=DocHelper(), doc_name=doc_name)
        # save the results of templating
        if file_type == 'html':
            subdir = 'html'
        else:
            subdir = ''
        doc_file = codecs.open(os.path.join(docs_output_path, subdir, doc_name + '.' + file_type), 'w','utf8')
        doc_file.write(doc)
        doc_file.close()


economy_schemas = {}
for economy in global_constants.economies:
    enabled_cargos = [cargo for cargo in registered_cargos if not cargo.economy_variations[economy].get('disabled')]
    enabled_industries = [industry for industry in registered_industries if industry.economy_variations[economy].enabled]
    economy_schemas[economy] = {'enabled_cargos':enabled_cargos, 'enabled_industries':enabled_industries}

# render standard docs from a list
html_docs = ['get_started', 'code_reference','economies', 'cargos', 'industries', 'translations']
txt_docs = ['changelog', 'license', 'readme', 'test_docs']

render_docs(html_docs, 'html')
render_docs(txt_docs, 'txt')
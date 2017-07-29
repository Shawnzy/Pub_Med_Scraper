import os
from lxml import etree
from lxml.etree import tostring
from itertools import chain
from .utils import *
from unidecode import unidecode


tree = read_xml(path)

    tree_title = tree.find('//title-group/article-title')
    if tree_title is not None:
        title = [t for t in tree_title.itertext()]
        sub_title = tree.xpath('//title-group/subtitle/text()')
        title.extend(sub_title)
        title = [t.replace('\n', ' ').replace('\t', ' ') for t in title]
        full_title = ' '.join(title)
    else:
        full_title = ''

    try:
        abstracts = list()
        abstract_tree = tree.findall('//abstract')
        for a in abstract_tree:
            for t in a.itertext():
                text = t.replace('\n', ' ').replace('\t', ' ').strip()
                abstracts.append(text)
        abstract = ' '.join(abstracts)
    except:
        abstract = ''

    journal_node = tree.findall('//journal-title')
    if journal_node is not None:
        journal = ' '.join([j.text for j in journal_node])
    else:
        journal = ''

    dict_article_meta = parse_article_meta(tree)
    pub_year_node = tree.find('//pub-date/year')
    pub_year = pub_year_node.text if pub_year_node is not None else ''

    subjects_node = tree.findall('//article-categories//subj-group/subject')
    subjects = list()
    if subjects_node is not None:
        for s in subjects_node:
            subject = ' '.join([s_.strip() for s_ in s.itertext()]).strip()
            subjects.append(subject)
        subjects = '; '.join(subjects)
    else:
        subjects = ''

    # create affiliation dictionary
    affil_id = tree.xpath('//aff[@id]/@id')
    if len(affil_id) > 0:
        affil_id = list(map(str, affil_id))
    else:
        affil_id = ['']  # replace id with empty list

    affil_name = tree.xpath('//aff[@id]')
    affil_name_list = list()
    for e in affil_name:
        name = stringify_affiliation_rec(e)
        name = name.strip().replace('\n', ' ')
        affil_name_list.append(name)
    affiliation_list = [[idx, name] for idx, name in zip(affil_id, affil_name_list)]

    tree_author = tree.xpath('//contrib-group/contrib[@contrib-type="author"]')
    author_list = list()
    for author in tree_author:
        author_aff = author.findall('xref[@ref-type="aff"]')
        try:
            ref_id_list = [str(a.attrib['rid']) for a in author_aff]
        except:
            ref_id_list = ''
        try:
            author_list.append([author.find('name/surname').text,
                                author.find('name/given-names').text,
                                ref_id_list])
        except:
            author_list.append(['', '', ref_id_list])
    author_list = flatten_zip_author(author_list)

    dict_out = {'full_title': full_title.strip(),
                'abstract': abstract,
                'journal': journal,
                'pmid': dict_article_meta['pmid'],
                'pmc': dict_article_meta['pmc'],
                'doi': dict_article_meta['doi'],
                'publisher_id': dict_article_meta['publisher_id'],
                'author_list': author_list,
                'affiliation_list': affiliation_list,
                'publication_year': pub_year,
                'subjects': subjects}
    if include_path:
        dict_out['path_to_file'] = path
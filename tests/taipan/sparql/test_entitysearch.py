"""Tests for taipan.sparql.entitysearch."""

from nose.tools import nottest

from taipan.sparql.entitysearch import retrieve_entity

@nottest
def test_retrieve_entity():
    """Timeout"""
    label = "Australia"
    entity = retrieve_entity(label)

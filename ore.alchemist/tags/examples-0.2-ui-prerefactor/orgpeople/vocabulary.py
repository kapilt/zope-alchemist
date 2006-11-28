"""
Define a vocabulary for states
$Id$ 
"""

from ore.alchemist.vocabulary import VocabularyTable
from schema import StateTable

StateVocabulary = VocabularyTable( StateTable, "state_code", "state_name" )

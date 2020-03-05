#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create wiktionary-like inflection tables for omorfi paradigms and words.
"""


from argparse import ArgumentParser, FileType
from random import choice
from sys import stderr, stdout
from time import perf_counter, process_time

from omorfi import Omorfi


def generate(generator, word, upos, omors=""):
    """Generate word-form."""
    wf = generator.generate("[WORD_ID=" + word + "][UPOS=" + upos + "]" +
                            omors)
    if not wf:
        return '---'
    else:
        return wf

def generate_negative_verb(person):
    return {
        "SG1": "en",
        "SG2": "et",
        "SG3": "ei",
        "PL1": "emme",
        "PL2": "ette",
        "PL3": "eivät",
    }[person]

def generate_simple_verb(omorfi, word, person, tense):
    spec = "[VOICE=ACT][MOOD=INDV][TENSE={tense}][PERS={person}]"
    return generate(omorfi, word, "VERB", spec.format(person=person, tense=tense))

def generate_negated_verb(omorfi, word, person, tense):
    negative_verb = generate_negative_verb(person)
    if tense == "PRESENT":
        spec = "[VOICE=ACT][MOOD=INDV][TENSE=PRESENT][NEG=CON]"
    elif tense == "PAST":
        spec = "[VOICE=ACT][MOOD=INDV][TENSE=PAST][NUM={pers}][NEG=CON]"
    conneg = generate(omorfi, word, "VERB", spec.format(pers=person[:2]))
    return negative_verb + " " + conneg

def generate_perfect_verb(omorfi, word, person, tense):
    spec = "[VOICE=ACT][MOOD=INDV][TENSE=PRESENT][PERS={person}]"
    verb = generate(omorfi, "olla_2", "VERB", spec.format(person=person))
    if tense == "PLUSQUAMPERFECT":
        if person[:2] == "SG":
            ollut = "ollut"
        elif person[:2] == "PL":
            ollut = "olleet"
        verb = verb + " " + ollut
    spec = "[VOICE=ACT][MOOD=INDV][TENSE=PAST][NUM={pers}][NEG=CON]"
    pcp = generate(omorfi, word, "VERB", spec.format(pers=person[:2]))
    return verb + " " + pcp

def generate_negated_perfect_verb(omorfi, word, person, tense):
    if tense == "PERFECT":
        verb = generate_negated_verb(omorfi, "olla_2", person, "PRESENT")
    else:
        verb = generate_negative_verb(person)
        if person[:2] == "SG":
            ollut = "ollut"
        elif person[:2] == "PL":
            ollut = "olleet"
        verb = verb + " " + ollut
    spec = "[VOICE=ACT][MOOD=INDV][TENSE=PAST][NUM={pers}][NEG=CON]"
    pcp = generate(omorfi, word, "VERB", spec.format(pers=person[:2]))
    return verb + " " + pcp


def test_loop(omorfi):
    words = ("maksaa", "ostaa", "tulla", "mennä")
    persons = {"minä": "SG1", "sinä": "SG2", "hän": "SG3", "me":"PL1", "te": "PL2", "he": "PL3"}
    tenses = {"present": "PRESENT", "imperfect": "PAST", "perfect": "PERFECT", "plusquamperfect": "PLUSQUAMPERFECT"}
    negatives = ("negated", "")
    while True:
        word, person, tense, negative = choice(words), choice(list(persons)), choice(list(tenses)), choice(negatives)
        print (word, person, tense, negative)
        if tense in ("perfect", "plusquamperfect"):
            if negative:
                answer = generate_negated_perfect_verb(omorfi, word, persons[person], tenses[tense])
            else:
                answer = generate_perfect_verb(omorfi, word, persons[person], tenses[tense])
        else:
            if negative:
                answer = generate_negated_verb(omorfi, word, persons[person], tenses[tense])
            else:
                answer = generate_simple_verb(omorfi, word, persons[person], tenses[tense])
        print("Tense {0} || {1}:\n {2} [{3}]".format(tense, negative, person, word.upper()))
        guess = input("What's the answer? ").strip()
        if guess == answer:
             print("Yes!")
        else:
             print("No - it should have been " + answer)
        print("\n----------------------------------------")
        

def main():
    omorfi = Omorfi()
    omorfi.load_generator("src/generated/omorfi.generate.hfst")
    test_loop(omorfi)

if __name__ == "__main__":
    main()

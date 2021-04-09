#!/usr/bin/env python3

""" Test Mapping langs utility functions and their use in g2p convert --check """

from unittest import TestCase, main

from g2p import make_g2p
from g2p.mappings.langs import utils


class LangsUtilsTest(TestCase):
    def test_is_IPA(self):
        self.assertTrue(utils.is_panphon("ijŋeːʒoːɡd͡ʒ"))  # All panphon chars
        self.assertTrue(utils.is_panphon("ij ij"))  # tokenizes on spaces
        # ASCII g is not ipa/panphon use ɡ (\u0261)
        self.assertFalse(utils.is_panphon("ga"))
        # ASCII : is not ipa/panphon, use ː (\u02D0)
        self.assertFalse(utils.is_panphon("e:"))

    def test_is_arpabet(self):
        arpabet_string = "S AH S IY  EH  AO N  T EH"
        non_arpabet_string = "sometext"
        self.assertTrue(utils.is_arpabet(arpabet_string))
        self.assertFalse(utils.is_arpabet(non_arpabet_string))

    def test_check_arpabet(self):
        transducer = make_g2p("eng-ipa", "eng-arpabet")
        self.assertTrue(transducer.check(transducer("jŋeːi")))
        self.assertFalse(transducer.check(transducer("gaŋi")))
        self.assertTrue(transducer.check(transducer("ɡɑŋi")))
        self.assertFalse(transducer.check(transducer("ñ")))

    def test_check_ipa(self):
        transducer = make_g2p("fra", "fra-ipa")
        self.assertTrue(transducer.check(transducer("ceci")))
        self.assertFalse(transducer.check(transducer("ñ")))
        self.assertTrue(transducer.check(transducer("ceci est un test été à")))

        transducer = make_g2p("fra-ipa", "eng-ipa")
        self.assertFalse(transducer.check(transducer("ñ")))

    def test_check_composite_transducer(self):
        transducer = make_g2p("fra", "eng-arpabet")
        self.assertTrue(transducer.check(transducer("ceci est un test été à")))
        self.assertFalse(transducer.check(transducer("ñ")))

    def test_check_tokenizing_transducer(self):
        transducer = make_g2p("fra", "fra-ipa", tok_lang="fra")
        self.assertTrue(transducer.check(transducer("ceci est un test été à")))
        self.assertFalse(transducer.check(transducer("ñ oǹ")))
        self.assertTrue(
            transducer.check(transducer("ceci, cela; c'est tokenizé: alors c'est bon!"))
        )
        self.assertFalse(
            transducer.check(transducer("mais... c'est ñoñ, si du texte ne passe pas!"))
        )

    def test_check_tokenizing_composite_transducer(self):
        transducer = make_g2p("fra", "eng-arpabet", tok_lang="fra")
        self.assertTrue(transducer.check(transducer("ceci est un test été à")))
        self.assertFalse(transducer.check(transducer("ñ oǹ")))
        self.assertTrue(
            transducer.check(transducer("ceci, cela; c'est tokenizé: alors c'est bon!"))
        )
        self.assertFalse(
            transducer.check(transducer("mais... c'est ñoñ, si du texte ne passe pas!"))
        )

    def test_shallow_check(self):
        transducer = make_g2p("win", "eng-arpabet", tok_lang="win")
        # This is False, but should be True! It's Flase because the mapping outputs :
        # instead of ː
        # self.assertFalse(transducer.check(transducer("uu")))
        self.assertTrue(transducer.check(transducer("uu"), shallow=True))

    def test_check_with_equiv(self):
        transducer = make_g2p("tau", "eng-arpabet", tok_lang="tau")
        self.assertTrue(transducer.check(transducer("sh'oo Jign maasee' do'eent'aa shyyyh")))

if __name__ == "__main__":
    main()
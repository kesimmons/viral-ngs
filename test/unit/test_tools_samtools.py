# Unit tests for tools.samtools

__author__ = "dpark@broadinstitute.org"

import unittest
import os
import tempfile
import shutil
import util
import util.file
import tools
import tools.samtools
from test import TestCaseWithTmp


class TestToolSamtools(TestCaseWithTmp):

    def test_count_bam(self):
        sam = os.path.join(util.file.get_test_input_path(self), 'simple.sam')
        n = tools.samtools.SamtoolsTool().count(sam, ['-S'])
        self.assertEqual(n, 2)

    def test_fasta_index(self):
        orig_ref = os.path.join(util.file.get_test_input_path(self), 'in.fasta')
        expected_fai = os.path.join(util.file.get_test_input_path(self), 'in.fasta.fai')
        samtools = tools.samtools.SamtoolsTool()
        for ext in ('.fasta', '.fa'):
            inRef = util.file.mkstempfname(ext)
            shutil.copyfile(orig_ref, inRef)
            outFai = inRef + '.fai'
            samtools.faidx(inRef)
            self.assertEqualContents(outFai, expected_fai)

    def test_isEmpty(self):
        samtools = tools.samtools.SamtoolsTool()
        self.assertTrue(samtools.isEmpty(os.path.join(util.file.get_test_input_path(), 'empty.bam')))
        self.assertFalse(samtools.isEmpty(os.path.join(util.file.get_test_input_path(), 'almost-empty.bam')))
        self.assertFalse(samtools.isEmpty(os.path.join(util.file.get_test_input_path(), 'G5012.3.subset.bam')))
        self.assertFalse(samtools.isEmpty(os.path.join(util.file.get_test_input_path(), 'G5012.3.testreads.bam')))

    def test_sam_downsample(self):
        desired_count = 100
        tolerance = 0.1

        in_sam = os.path.join(util.file.get_test_input_path(), 'G5012.3.subset.bam')
        out_bam = util.file.mkstempfname('.bam')

        samtools = tools.samtools.SamtoolsTool()

        samtools.downsample_to_approx_count(in_sam, out_bam, desired_count)

        assert samtools.count(out_bam) in range(
            int(desired_count - (desired_count * tolerance)), int(desired_count + (desired_count * tolerance))+1
        ), "Downsampled bam file does not contain the expected number of reads within tolerance: %s" % tolerance

#!/usr/bin/env python3

from collections import OrderedDict
from enum import Enum

from bin_addr import BinaryAddress
from word_addr import WordAddress


# An address reference consisting of the address and all of its components
class Reference(object):

    def __init__(self, word_addr, num_addr_bits,
                 num_offset_bits, num_index_bits, num_tag_bits):
        self.word_addr = WordAddress(word_addr)
        # BinaryAddress를 통해 WordAddr를 더 쉽게 만들고 추출하기 쉬운 메서드 제공
        # ex 180 -> 1011 0100 여기서 오프셋, 인덱스, 테그 추출
        self.bin_addr = BinaryAddress(
            word_addr=self.word_addr, num_addr_bits=num_addr_bits)
        self.offset = self.bin_addr.get_offset(num_offset_bits)
        self.index = self.bin_addr.get_index(num_offset_bits, num_index_bits)
        self.tag = self.bin_addr.get_tag(num_tag_bits)
        self.cache_status = None

    def __str__(self):
        return str(OrderedDict(sorted(self.__dict__.items())))

    __repr__ = __str__

    # Return a lightweight entry to store in the cache
    def get_cache_entry(self, num_words_per_block):
        return {
            'tag': self.tag,
            'data': self.word_addr.get_consecutive_words(
                num_words_per_block)
        }


# An enum representing the cache status of a reference (i.e. hit or miss)
class ReferenceCacheStatus(Enum):

    miss = 0
    hit = 1
    hit_2l = 2

    # Define how reference statuses are displayed in simulation results
    def __str__(self):
        if self.value == ReferenceCacheStatus.hit.value:
            return '1-level-HIT'
        elif self.value == ReferenceCacheStatus.hit_2l.value:
            return '2-level-Hit'
        else:
            return 'miss'

    __repr__ = __str__

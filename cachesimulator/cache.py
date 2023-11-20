#!/usr/bin/env python3

from bin_addr import BinaryAddress
from reference import ReferenceCacheStatus
from word_addr import WordAddress


class Cache(dict):

    # Initializes the reference cache with a fixed number of sets
    def __init__(self, cache=None, num_sets=None, num_index_bits=0):

        # A list of recently ordered addresses, ordered from least-recently
        # used to most
        self.recently_used_addrs = []

        #캐시가 있으면 해당 캐시로 초기화 하고
        #없으면 세트 개수 만큼 생성하여 초기화 한다.
        #세트가 한개이고 인덱스가 3비트이면 8개 만큼 생성될듯
        if cache is not None:
            self.update(cache)
        else:
            for i in range(num_sets):
                index = BinaryAddress(
                    word_addr=WordAddress(i), num_addr_bits=num_index_bits)
                #자기 자신을 배열로 선언?
                self[index] = []

    # Every time we see an address, place it at the top of the
    # list of recently-seen addresses
    def mark_ref_as_last_seen(self, ref):

        # The index and tag (not the offset) uniquely identify each address
        addr_id = (ref.index, ref.tag)
        if addr_id in self.recently_used_addrs:
            self.recently_used_addrs.remove(addr_id)
        self.recently_used_addrs.append(addr_id)

    # Returns True if a block at the given index and tag exists in the cache,
    # indicating a hit; returns False otherwise, indicating a miss
    def is_hit(self, addr_index, addr_tag):

        # Ensure that indexless fully associative caches are accessed correctly
        if addr_index is None:
            blocks = self['0']
        elif addr_index in self:
            blocks = self[addr_index]
        else:
            return False

        for block in blocks:
            if block['tag'] == addr_tag:
                return True

        return False

    # Iterate through the recently-used entries in reverse order for MRU
    def replace_block(self, blocks, replacement_policy, addr_index, new_entry):
        if replacement_policy == 'mru':
            recently_used_addrs = reversed(self.recently_used_addrs)
        else:
            recently_used_addrs = self.recently_used_addrs
        # Replace the first matching entry with the entry to add
        for recent_index, recent_tag in recently_used_addrs:
            for i, block in enumerate(blocks):
                if (recent_index == addr_index and
                        block['tag'] == recent_tag):
                    blocks[i] = new_entry
                    return

    # Adds the given entry to the cache at the given index
    def set_block(self, replacement_policy,
                  num_blocks_per_set, addr_index, new_entry):
        # Place all cache entries in a single set if cache is fully associative
        if addr_index is None:
            blocks = self['0']
        else:
            blocks = self[addr_index]
        # Replace MRU or LRU entry if number of blocks in set exceeds the limit
        if len(blocks) == num_blocks_per_set:
            self.replace_block(
                blocks, replacement_policy, addr_index, new_entry)
        else:
            blocks.append(new_entry)

    # Simulate the cache by reading the given address references into it
    def read_refs(self, num_blocks_per_set,
                  num_words_per_block, replacement_policy, refs, cache_2l):

        for ref in refs:
            self.mark_ref_as_last_seen(ref)

            # Record if the reference is already in the cache or not
            if self.is_hit(ref.index, ref.tag):
                # Give emphasis to hits in contrast to misses
                ref.cache_status = ReferenceCacheStatus.hit
            else:
                self.set_block(
                    replacement_policy=replacement_policy,
                    num_blocks_per_set=num_blocks_per_set,
                    addr_index=ref.index,
                    new_entry=ref.get_cache_entry(num_words_per_block))
                
                cache_2l.mark_ref_as_last_seen(ref)

                if cache_2l.is_hit(ref.index, ref.tag):
                    ref.cache_status = ReferenceCacheStatus.hit_2l
                else:
                    cache_2l.set_block(
                        replacement_policy=replacement_policy,
                        num_blocks_per_set=num_blocks_per_set,
                        addr_index=ref.index,
                        new_entry=ref.get_cache_entry(num_words_per_block))
                    ref.cache_status = ReferenceCacheStatus.miss
                    
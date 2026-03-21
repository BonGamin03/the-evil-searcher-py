import random
from typing import Any, List, Optional, Tuple
class Node:
 

    def __init__(self, val, freq: int = 0):
        self.val    = val
        self.freq   = freq
        self.prev   = None      
        self.next   = None       
        self.top    = None     
        self.bottom = None  


class SkipList:
 

    def __init__(self, max_levels: int = 16, prob: float = 0.5):
        self.max_levels = max_levels
        self.prob       = prob

 
        self.head = Node(float('-inf'))    
        self.tail = Node(float('+inf'))           
        self.head.next = self.tail
        self.tail.prev = self.head

        self.current_levels = 1   
        self.size           = 0   

    
    def search(self, root: Optional[Node], target: Any) -> bool:
        """
        Find `target` starting on `root`.
        """
        if root is None:
            return False
        if root.val == target:
            return True

        c = root
        while c is not None:
            
            while c.next is not None and c.next.val <= target:
                c = c.next

           
            if c.val == target:
                return True

           
            c = c.bottom

        return False

    def _update_existing_freq(self, val: Any, freq: int) -> bool:
        """Update freq for an existing value across all levels.

        Returns True if the value was found and updated.
        """
        c = self.head
        updated = False
        while c is not None:
            while c.next is not None and c.next.val < val:
                c = c.next

            if c.next is not None and c.next.val == val:
                c.next.freq = freq
                updated = True

            c = c.bottom

        return updated
    
    def _random_level(self) -> int:
        """
        Cant levels for new node
        Return: int range [ 1 :max_levels].
        """
        level = 1
        while random.random() < self.prob and level < self.max_levels:
            level += 1
        return level

    def insert(self, val: Any, freq: int = 1) -> None:
        """
        Inser `val` order.
 
        """
        if self.search(self.head, val):
            self._update_existing_freq(val, freq)
            return

        # Build the search path (predecessors) from top level down to base level.
        # update[0] is top-level predecessor; update[-1] is base-level predecessor.
        update: List[Node] = []
        c = self.head
        while c is not None:
            while c.next is not None and c.next.val < val:
                c = c.next
            update.append(c)
            c = c.bottom

        new_level = self._random_level()

        # If we need more levels, add new empty levels on top and extend update accordingly.
        if new_level > self.current_levels:
            for _ in range(self.current_levels, new_level):
                new_head = Node(float('-inf'))
                new_tail = Node(float('+inf'))
                new_head.next = new_tail
                new_tail.prev = new_head

                new_head.bottom = self.head
                self.head.top = new_head
                new_tail.bottom = self.tail
                self.tail.top = new_tail

                self.head = new_head
                self.tail = new_tail

                # Predecessor on a new empty top level is always the new head.
                update.insert(0, new_head)

            self.current_levels = new_level

        # Insert from base level upwards so vertical links are consistent:
        # upper.bottom -> lower and lower.top -> upper.
        lower_node: Optional[Node] = None
        for level_offset in range(1, new_level + 1):
            pred = update[-level_offset]
            succ = pred.next

            new_node = Node(val, freq=freq)
            new_node.prev = pred
            new_node.next = succ
            pred.next = new_node
            if succ is not None:
                succ.prev = new_node

            new_node.bottom = lower_node
            if lower_node is not None:
                lower_node.top = new_node
            lower_node = new_node

        self.size += 1

    def _base_level_head(self) -> Node:
         
        node = self.head
        while node.bottom is not None:
            node = node.bottom
        return node
    
    
    
    
    def intersect(self, other: 'SkipList') -> 'SkipList':
        """
        Intersect two SkipList using the skip pointers.

        """
        result = SkipList(max_levels=self.max_levels, prob=self.prob)

        p1 = self._base_level_head().next
        end = float('+inf')

        while p1.val != end:
            # Buscar p1.val en `other` usando la búsqueda multinivel
            intersect_node=other.search(other.head, p1.val)
            if intersect_node:
                result.insert(p1.val,p1.freq+intersect_node.freq)
            p1 = p1.next

        return result

    def to_postings(self) -> List[Tuple[Any, int]]:
        """Return base-level postings as (val, freq) pairs."""
        result: List[Tuple[Any, int]] = []
        c = self._base_level_head().next
        while c is not None and c.val != float('+inf'):
            result.append((c.val, c.freq))
            c = c.next
        return result
    
    def to_list(self) -> List[Any]:
        """Devuelve todos los valores en orden ascendente desde el nivel base."""
        result = []
        c = self._base_level_head().next
        while c is not None and c.val != float('+inf'):
            result.append(c.val)
            c = c.next
        return result
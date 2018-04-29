class Trie:
    class Node:
        def __init__(self):
            self.nodes = {}
            self.is_end = False

    def __init__(self):
        self.root = self.Node()
        self.size = 0

    def add(self, string):
        curr = self.root
        self.size += 1
        for i in range(len(string)):
            if string[i] not in curr.nodes:
                curr.nodes[string[i]] = self.Node()
            if i == len(string) - 1:
                curr.nodes[string[i]].is_end = True
            curr = curr.nodes[string[i]]

    def contains(self, string):
        curr = self.root
        for i in range(len(string)):
            if string[i] not in curr.nodes:
                return False
            if i == len(string) - 1 and not curr.nodes[string[i]].is_end:
                return False
            curr = curr.nodes[string[i]]
        return True

    def remove(self, string):
        if self.recursive_remove(string, self.root, 0):
            self.size -= 1

    def recursive_remove(self, string, curr, i):
        if string[i] not in curr.nodes:
            return False
        if i == len(string) - 1:
            if curr.nodes[string[i]].is_end:
                if len(curr.nodes[string[i]].nodes) <= 0:
                    del curr.nodes[string[i]]
                else:
                    curr.nodes[string[i]].is_end = False
                return True
            return False
        can_remove = self.recursive_remove(string, curr.nodes[string[i]], i + 1)
        if can_remove and len(curr.nodes[string[i]].nodes) <= 0:
            del curr.nodes[string[i]]
        return can_remove

    def all_words(self):
        return self.recursive_all_words(self.root, "", [])

    def recursive_all_words(self, curr, word, res):
        if curr.is_end:
            res.append(word)
        for key in curr.nodes:
            self.recursive_all_words(curr.nodes[key], word + key, res)
        return res

    def all_words_with_prefix(self, string):
        curr = self.root
        for i in range(len(string)):
            if string[i] not in curr.nodes:
                return []
            curr = curr.nodes[string[i]]
        return self.recursive_all_words(curr, string, [])

trie = Trie()
trie.add("hello")
trie.add("he")
trie.add("her")
trie.add("apple")
trie.add("alias")
trie.add("zebra")
trie.add("code")
trie.add("corporation")
print(trie.contains("hi"))
print(trie.contains("coder"))
print(trie.contains("z"))
print(trie.contains("ze"))
print(trie.contains("zebra"))
print(trie.contains("her"))
trie.remove("her")
print(trie.contains("her"))
print(trie.contains("he"))
trie.remove("he")
print(trie.contains("he"))
print(trie.contains("hello"))
print(trie.all_words())
print(trie.all_words_with_prefix("co"))

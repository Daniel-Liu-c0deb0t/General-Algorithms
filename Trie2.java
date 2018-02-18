import java.util.ArrayList;

public class Trie2{
	int size = 0;
	Node root = new Node();
	
	public static void main(String[] args){
		Trie2 t = new Trie2();
		t.add("he");
		t.add("him");
		t.add("her");
		System.out.println(t.contains("her"));
		System.out.println(t.contains("how"));
		t.add("why");
		t.add("hello");
		t.add("world");
		System.out.println(t.contains("he"));
		System.out.println(t.contains("wh"));
		t.remove("hello");
		System.out.println(t.contains("hello"));
		t.add("how");
		System.out.println(t.allWords().toString());
		System.out.println(t.allWordsPrefix("he").toString());
	}
	
	class Node{
		Node[] n = new Node[26];
		boolean isEnd = false;
	}
	
	void add(String s){
		Node curr = root;
		size++;
		for(int i = 0; i < s.length(); i++){
			if(curr.n[s.charAt(i) - 'a'] == null)
				curr.n[s.charAt(i) - 'a'] = new Node();
			if(i == s.length() - 1)
				curr.n[s.charAt(i) - 'a'].isEnd = true;
			curr = curr.n[s.charAt(i) - 'a'];
		}
	}
	
	boolean contains(String s){
		Node curr = root;
		for(int i = 0; i < s.length(); i++){
			if(curr.n[s.charAt(i) - 'a'] == null)
				return false;
			if(i == s.length() - 1 && !curr.n[s.charAt(i) - 'a'].isEnd)
				return false;
			curr = curr.n[s.charAt(i) - 'a'];
		}
		return true;
	}
	
	void remove(String s){
		if(recursiveRemove(s, root, 0))
			size--;
	}
	
	boolean recursiveRemove(String s, Node curr, int i){
		if(curr.n[s.charAt(i) - 'a'] == null)
			return false;
		if(i == s.length() - 1){
			if(curr.n[s.charAt(i) - 'a'].isEnd){
				curr.n[s.charAt(i) - 'a'].isEnd = false;
				return true;
			}
			return false;
		}
		return recursiveRemove(s, curr.n[s.charAt(i) - 'a'], i + 1);
	}
	
	ArrayList<String> allWords(){
		return recursiveAllWords(root, new StringBuilder(), new ArrayList<String>());
	}
	
	ArrayList<String> allWordsPrefix(String s){
		Node curr = root;
		for(int i = 0; i < s.length(); i++){
			if(curr.n[s.charAt(i) - 'a'] == null){
				return new ArrayList<String>();
			}
			curr = curr.n[s.charAt(i) - 'a'];
		}
		return recursiveAllWords(curr, new StringBuilder(s), new ArrayList<String>());
	}
	
	ArrayList<String> recursiveAllWords(Node curr, StringBuilder s, ArrayList<String> res){
		if(curr == null)
			return res;
		if(curr.isEnd)
			res.add(s.toString());
		for(int i = 0; i < curr.n.length; i++){
			recursiveAllWords(curr.n[i], s.append((char)(i + 'a')), res);
			s.deleteCharAt(s.length() - 1);
		}
		return res;
	}
}

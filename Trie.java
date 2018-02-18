import java.util.ArrayList;

public class Trie<T> {
	private Node<T> root = new Node<T>(null);
	
	public void add(String key, T val){
		Node<T> curr = root;
		for(int i = 0; i < key.length(); i++){
			if(curr.get(key.charAt(i)) == null){
				curr.set(key.charAt(i), new Node<T>(null));
			}
			if(i == key.length() - 1){
				curr.get(key.charAt(i)).val = val;
			}
			curr = curr.get(key.charAt(i));
		}
	}
	
	public boolean contains(String key){
		Node<T> curr = root;
		for(int i = 0; i < key.length(); i++){
			if(curr.get(key.charAt(i)) == null){
				return false;
			}
			if(i == key.length() - 1 && curr.get(key.charAt(i)).val == null){
				return false;
			}
			curr = curr.get(key.charAt(i));
		}
		return true;
	}
	
	public T get(String key){
		Node<T> curr = root;
		for(int i = 0; i < key.length(); i++){
			if(curr.get(key.charAt(i)) == null){
				return null;
			}
			if(i == key.length() - 1){
				if(curr.get(key.charAt(i)).val != null){
					return curr.get(key.charAt(i)).val;
				}else{
					return null;
				}
			}
			curr = curr.get(key.charAt(i));
		}
		return null;
	}
	
	public ArrayList<String> inorderKeys(){
		return recursiveInorderKeys(root, new StringBuilder(), new ArrayList<String>());
	}
	
	private ArrayList<String> recursiveInorderKeys(Node<T> curr, StringBuilder builder, ArrayList<String> result){
		if(curr == null){
			return result;
		}
		if(curr.val != null){
			result.add(builder.toString());
		}
		for(int i = 0; i < curr.nodes.size(); i++){
			recursiveInorderKeys(curr.nodes.get(i), builder.append((char)('a' + i)), result);
			builder.deleteCharAt(builder.length() - 1);
		}
		return result;
	}
	
	private class Node<E>{
		ArrayList<Node<E>> nodes = new ArrayList<Node<E>>();
		E val;
		
		public Node(E val){
			this.val = val;
		}
		
		public Node<E> get(char c){
			if(c - 'a' >= nodes.size())
				return null;
			return nodes.get(c - 'a');
		}
		
		public void set(char c, Node<E> val){
			while(c - 'a' >= nodes.size()){
				nodes.add(null);
			}
			nodes.set(c - 'a', val);
		}
	}
	
	public static void main(String[] args){
		Trie<String> trie = new Trie<String>();
		trie.add("aaaa", "1");
		trie.add("bbbb", "2");
		trie.add("atcg", "3");
		trie.add("gtca", "4");
		trie.add("agtc", "5");
		trie.add("gggg", "6");
		trie.add("ggcg", "7");
		System.out.println(trie.contains("aaaa"));
		System.out.println(trie.contains("atcg"));
		System.out.println(trie.contains("ggggg"));
		System.out.println(trie.get("aaaa"));
		System.out.println(trie.get("atcg"));
		System.out.println(trie.get("ggcg"));
		ArrayList<String> result = trie.inorderKeys();
		System.out.println(result);
	}
}

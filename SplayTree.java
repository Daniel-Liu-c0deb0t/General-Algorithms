
public class SplayTree{
	Node nullNode, root;
	int size;
	
	public static void main(String[] args){
		int[] arr = {1, 2, 3, 4, 5};
		SplayTree t = new SplayTree(arr);
		t.reverse(1, 3);
		t.addRange(0, 4, 1);
		t.revolve(0, 4, 1);
		t.remove(4);
		System.out.println(t.min(2, 3));
		for(int i = 0; i < t.size - 2; i++){
			System.out.print(t.min(i, i) + " ");
		}
		System.out.println();
	}
	
	SplayTree(int[] arr){
		nullNode = new Node();
		nullNode.reverse = false;
		nullNode.parent = nullNode;
		nullNode.c[0] = nullNode;
		nullNode.c[1] = nullNode;
		nullNode.size = 0;
		nullNode.min = Integer.MAX_VALUE;
		
		int[] s = new int[arr.length + 2];
		System.arraycopy(arr, 0, s, 1, arr.length);
		
		size = arr.length;
		s[0] = Integer.MAX_VALUE;
		s[size + 1] = Integer.MAX_VALUE;
		size += 2;
		root = construct(s, nullNode, 0, size - 1);
	}
	
	Node construct(int[] s, Node parent, int l, int r){
		if(l > r)
			return nullNode;
		int mid = (l + r) >>> 1;
		Node x = newNode(parent, s[mid]);
		x.c[0] = construct(s, x, l, mid - 1);
		x.c[1] = construct(s, x, mid + 1, r);
		up(x);
		return x;
	}
	
	void up(Node x){
		x.size = x.c[0].size + x.c[1].size + 1;
		x.min = Math.min(x.c[0].min, Math.min(x.c[1].min, x.value));
	}
	
	void reverse(Node x){
		if(x == nullNode)
			return;
		x.reverse = !x.reverse;
		Node t = x.c[0];
		x.c[0] = x.c[1];
		x.c[1] = t;
	}
	
	void add(Node x, int val){
		if(x == nullNode)
			return;
		x.add += val;
		x.value += val;
		if(x.min < Integer.MAX_VALUE)
			x.min += val;
	}
	
	void down(Node x){
		if(x.reverse){
			reverse(x.c[0]);
			reverse(x.c[1]);
			x.reverse = false;
		}
		if(x.add != 0){
			add(x.c[0], x.add);
			add(x.c[1], x.add);
			x.add = 0;
		}
	}
	
	Node newNode(Node parent, int val){
		Node x = new Node();
		x.c[0] = nullNode;
		x.c[1] = nullNode;
		x.parent = parent;
		x.value = val;
		x.size = 1;
		x.reverse = false;
		x.min = val;
		return x;
	}
	
	void rotate(Node x, int type){
		Node y = x.parent;
		down(y);
		down(x);
		x.parent = y.parent;
		if(y.parent != nullNode){
			if(y.parent.c[0] == y){
				y.parent.c[0] = x;
			}else{
				y.parent.c[1] = x;
			}
		}
		y.parent = x;
		y.c[type ^ 1] = x.c[type];
		if(x.c[type] != nullNode){
			x.c[type].parent = y;
		}
		x.c[type] = y;
		up(y);
	}
	
	void splay(Node x, Node p){
		for(down(x); x.parent != p;){
			if(x.parent.parent == p){
				if(x.parent.c[0] == x)
					rotate(x, 1);
				else
					rotate(x, 0);
			}else{
				Node y = x.parent;
				Node z = y.parent;
				if(y.c[0] == x){
					if(z.c[0] == y){
						rotate(y, 1);
						rotate(x, 1);
					}else{
						rotate(x, 1);
						rotate(x, 0);
					}
				}else{
					if(z.c[0] == y){
						rotate(x, 0);
						rotate(x, 1);
					}else{
						rotate(y, 0);
						rotate(x, 0);
					}
				}
			}
		}
		up(x);
		if(p == nullNode)
			root = x;
	}
	
	void select(int k, Node f){
		Node x = root;
		while(x != nullNode){
			down(x);
			int t = x.c[0].size;
			if(t + 1 == k)
				break;
			if(k <= t)
				x = x.c[0];
			else{
				k -= t + 1;
				x = x.c[1];
			}
		}
		splay(x, f);
	}
	
	void addRange(int l, int r, int v){
		l += 2;
		r += 2;
		select(l - 1, nullNode);
		select(r + 1, root);
		add(root.c[1].c[0], v);
		splay(root.c[1], nullNode);
	}
	
	void reverse(int l, int r){
		l += 2;
		r += 2;
		select(l - 1, nullNode);
		select(r + 1, root);
		reverse(root.c[1].c[0]);
	}
	
	void revolve(int l, int r, int t){
		l += 2;
		r += 2;
		t %= r - l + 1;
		select(r - t, nullNode);
		select(r + 1, root);
		Node x = root.c[1].c[0];
		root.c[1].c[0] = nullNode;
		select(l - 1, nullNode);
		select(l, root);
		root.c[1].c[0] = x;
		x.parent = root.c[1];
	}
	
	void insert(int x, int P){
		x += 2;
		size++;
		select(x, nullNode);
		select(x + 1, root);
		root.c[1].c[0] = newNode(root.c[1], P);
		splay(root.c[1].c[0], nullNode);
	}
	
	void remove(int x){
		x += 2;
		size--;
		select(x - 1, nullNode);
		select(x + 1, root);
		root.c[1].c[0] = nullNode;
		splay(root.c[1], nullNode);
	}
	
	int min(int l, int r){
		l += 2;
		r += 2;
		select(l - 1, nullNode);
		select(r + 1, root);
		return root.c[1].c[0].min;
	}
	
	class Node{
		int size, value, min, add;
		boolean reverse;
		Node parent, c[] = new Node[2];
	}
}

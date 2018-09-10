
public class DynamicSegmentTreeLazy{
    int n;
    int emptyQuery = 0;
	Node root = new Node(emptyQuery);
	
	public static void main(String[] args){
        DynamicSegmentTreeLazy t = new DynamicSegmentTreeLazy(Integer.MAX_VALUE >> 1);
		t.update(t.root, 0, t.n - 1, 10000, 100000, 0, 10);
		t.update(t.root, 0, t.n - 1, 20000, 100000, 0, 10);
        System.out.println(t.query(t.root, 0, t.n - 1, 1000, 1000000, 0));
	}
	
	DynamicSegmentTreeLazy(int n){
		this.n = n;
	}
	
	int combineQuery(int a, int b){
		return a + b;
	}
	
	int combineUpdate(int o, int val){
		return o + val;
	}
	
	int combineUpdateRange(int l, int r, int o, int val){
		return o + (r - l + 1) * val;
	}
	
	boolean updateBreak(int i, int val){
		return false;
	}
	
	boolean updateCondition(int i, int val){
		return true;
	}
	
	void tag(Node curr, int l, int r){
		if(curr.lazy != 0){
			curr.val = combineUpdateRange(l, r, curr.val, curr.lazy);
			if(l != r){
                if(curr.left == null) curr.left = new Node(emptyQuery);
                curr.left.lazy = combineUpdate(curr.left.lazy, curr.lazy);
                if(curr.right == null) curr.right = new Node(emptyQuery);
                curr.right.lazy = combineUpdate(curr.right.lazy, curr.lazy);
			}
			curr.lazy = 0;
		}
	}
	
	int query(Node curr, int l, int r, int ql, int qr, int i){
		if(curr == null || r < ql || l > qr){
			return emptyQuery;
		}
		
		tag(curr, l, r);
		
		if(l >= ql && qr >= r){
			return curr.val;
		}
		
		int m = (l + r) >>> 1;
		return combineQuery(query(curr.left, l, m, ql, qr, i * 2 + 1), query(curr.right, m + 1, r, ql, qr, i * 2 + 2));
	}
	
	void update(Node curr, int l, int r, int ul, int ur, int i, int val){
		tag(curr, l, r);
		
		if(r < ul || l > ur || updateBreak(i, val)){
			return;
		}
		
		if(l >= ul && r <= ur && updateCondition(i, val)){
			curr.val = combineUpdateRange(l, r, curr.val, val);
			if(l != r){
                if(curr.left == null) curr.left = new Node(emptyQuery);
                curr.left.lazy = combineUpdate(curr.left.lazy, val);
                if(curr.right == null) curr.right = new Node(emptyQuery);
				curr.right.lazy = combineUpdate(curr.right.lazy, val);
			}
			return;
		}
		
        int m = (l + r) >>> 1;
        if(curr.left == null) curr.left = new Node(emptyQuery);
        update(curr.left, l, m, ul, ur, i * 2 + 1, val);
        if(curr.right == null) curr.right = new Node(emptyQuery);
		update(curr.right, m + 1, r, ul, ur, i * 2 + 2, val);
		curr.val = combineQuery(curr.left.val, curr.right.val);
	}
    
    private class Node{
        int val, lazy = 0;
        Node left = null, right = null;

        Node(int val){
            this.val = val;
        }
    }
}
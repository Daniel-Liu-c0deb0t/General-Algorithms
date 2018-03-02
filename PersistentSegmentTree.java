import java.util.Random;

public class PersistentSegmentTree{
	int n;
	int[] seg;
	int[] left;
	int[] right;
	int nodeIdx;
	
	public static void main(String[] args){
		//must keep track of the version of the tree
		int iter = 100000;
		int v = -1;
		PersistentSegmentTree st = new PersistentSegmentTree(iter);
		v = st.construct(0, iter - 1, 0);
		Random r = new Random();
		for(int i = 0; i < iter; i++)
			v = st.update(0, iter - 1, i, v, i % 2 == 0 ? r.nextInt(5000) : 5000 + r.nextInt(5000));
		for(int i = 0; i < iter; i++)
			st.query(0, iter - 1, 0, i, v);
		System.out.println(st.query(0, iter - 1, 0, iter - 1, v));
		
		PersistentSegmentTree st2 = new PersistentSegmentTree(5);
		v = st2.construct(0, 5 - 1, 0);
		v = st2.update(0, 5 - 1, 1, v, 3);
		v = st2.update(0, 5 - 1, 2, v, 2);
		System.out.println(st2.query(0, 5 - 1, 0, 2, v));
	}
	
	PersistentSegmentTree(int n){
		this.n = n;
		this.seg = new int[n * 8 * 31];
		this.left = new int[n * 8 * 31];
		this.right = new int[n * 8 * 31];
		this.nodeIdx = 0;
	}
	
	int emptyQuery = 0;
	
	int combineQuery(int a, int b){
		return a + b;
	}
	
	int combineUpdate(int o, int val){
		return o + val;
	}
	
	//nodeIdx = 0 is the null value
	int createLeaf(int val){
		nodeIdx++;
		left[nodeIdx] = 0;
		right[nodeIdx] = 0;
		seg[nodeIdx] = val;
		return nodeIdx;
	}
	
	int createParent(int l, int r){
		nodeIdx++;
		left[nodeIdx] = l;
		right[nodeIdx] = r;
		seg[nodeIdx] = combineQuery(seg[l], seg[r]);
		return nodeIdx;
	}
	
	int construct(int[] arr, int l, int r){
		if(l == r){
			return createLeaf(arr[l]);
		}
		int m = (l + r) >>> 1;
		return createParent(construct(arr, l, m), construct(arr, m + 1, r));
	}
	
	int construct(int l, int r, int val){
		if(l == r){
			return createLeaf(val);
		}
		int m = (l + r) >>> 1;
		return createParent(construct(l, m, val), construct(m + 1, r, val));
	}
	
	int query(int l, int r, int ql, int qr, int i){
		if(l >= ql && qr >= r){
			return seg[i];
		}
		if(r < ql || l > qr){
			return emptyQuery;
		}
		int m = (l + r) >>> 1;
		return combineQuery(query(l, m, ql, qr, left[i]), query(m + 1, r, ql, qr, right[i]));
	}
	
	int update(int l, int r, int ui, int i, int val){
		if(l == r){
			return createLeaf(combineUpdate(seg[i], val));
		}
		int m = (l + r) >>> 1;
		if(ui <= m)
			return createParent(update(l, m, ui, left[i], val), right[i]);
		else
			return createParent(left[i], update(m + 1, r, ui, right[i], val));
	}
}

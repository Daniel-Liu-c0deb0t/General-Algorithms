
public class PersistentSegmentTreeLazy{
	int n;
	int[] seg;
	int[] left;
	int[] right;
	int[] lazy;
	int nodeIdx;
	
	public static void main(String[] args){
		int[] arr = {1, 2, 3, 4, 5};
		int v = -1;
		PersistentSegmentTreeLazy st = new PersistentSegmentTreeLazy(arr.length);
		v = st.construct(arr, 0, arr.length - 1);
		v = st.update(0, arr.length - 1, 0, 4, v, 3);
		System.out.println(st.query(0, arr.length - 1, 0, 4, v));
	}
	
	PersistentSegmentTreeLazy(int n){
		this.n = n;
		this.seg = new int[n * 8 * 31];
		this.left = new int[n * 8 * 31];
		this.right = new int[n * 8 * 31];
		this.lazy = new int[n * 8 * 31];
		this.nodeIdx = 0;
	}
	
	int emptyQuery = 0;
	
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
	
	void tag(int l, int r, int i){
		if(lazy[i] != 0){
			if(l != r){
				int m = (l + r) >>> 1;
				left[i] = createLazyChild(l, m, left[i], lazy[i]);
				right[i] = createLazyChild(m + 1, r, right[i], lazy[i]);
			}
			lazy[i] = 0;
		}
	}
	
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
	
	int createLazyChild(int l, int r, int i, int val){
		nodeIdx++;
		left[nodeIdx] = left[i];
		right[nodeIdx] = right[i];
		lazy[nodeIdx] = combineUpdate(lazy[i], val);
		seg[nodeIdx] = combineUpdateRange(l, r, seg[i], val);
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
		if(r < ql || l > qr){
			return emptyQuery;
		}
		if(l >= ql && qr >= r){
			return seg[i];
		}
		tag(l, r, i);
		
		int m = (l + r) >>> 1;
		return combineQuery(query(l, m, ql, qr, left[i]), query(m + 1, r, ql, qr, right[i]));
	}
	
	int update(int l, int r, int ul, int ur, int i, int val){
		if(r < ul || l > ur || updateBreak(i, val)){
			return i;
		}
		if(l >= ul && r <= ur && updateCondition(i, val)){
			return createLazyChild(l, r, i, val);
		}
		tag(l, r, i);
		
		int m = (l + r) >>> 1;
		return createParent(update(l, m, ul, ur, left[i], val), update(m + 1, r, ul, ur, right[i], val));
	}
}

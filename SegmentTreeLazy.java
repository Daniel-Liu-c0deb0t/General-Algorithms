
public class SegmentTreeLazy{
	int n;
	int[] seg;
	int[] lazy;
	
	public static void main(String[] args){
		int[] arr = {1, 2, 3, 4, 5};
		SegmentTreeLazy st = new SegmentTreeLazy(arr.length);
		st.construct(arr, 0, arr.length - 1, 0);
		st.update(0, arr.length - 1, 1, 2, 0, 3);
		System.out.println(st.query(0, arr.length - 1, 0, 2, 0));
	}
	
	SegmentTreeLazy(int n){
		this.n = n;
		seg = new int[n * 4];
		lazy = new int[n * 4];
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
			seg[i] = combineUpdateRange(l, r, seg[i], lazy[i]);
			if(l != r){
				lazy[i * 2 + 1] = combineUpdate(lazy[i * 2 + 1], lazy[i]);
				lazy[i * 2 + 2] = combineUpdate(lazy[i * 2 + 2], lazy[i]);
			}
			lazy[i] = 0;
		}
	}
	
	int construct(int[] arr, int l, int r, int i){
		if(l == r){
			seg[i] = arr[l];
			return seg[i];
		}
		int m = (l + r) >>> 1;
		seg[i] = combineQuery(construct(arr, l, m, i * 2 + 1), construct(arr, m + 1, r, i * 2 + 2));
		return seg[i];
	}
	
	int query(int l, int r, int ql, int qr, int i){
		tag(l, r, i);
		
		if(r < ql || l > qr){
			return emptyQuery;
		}
		if(l >= ql && qr >= r){
			return seg[i];
		}
		int m = (l + r) >>> 1;
		return combineQuery(query(l, m, ql, qr, i * 2 + 1), query(m + 1, r, ql, qr, i * 2 + 2));
	}
	
	void update(int l, int r, int ul, int ur, int i, int val){
		tag(l, r, i);
		
		if(r < ul || l > ur || updateBreak(i, val)){
			return;
		}
		if(l >= ul && r <= ur && updateCondition(i, val)){
			seg[i] = combineUpdateRange(l, r, seg[i], val);
			if(l != r){
				lazy[i * 2 + 1] = combineUpdate(lazy[i * 2 + 1], val);
				lazy[i * 2 + 2] = combineUpdate(lazy[i * 2 + 2], val);
			}
			return;
		}
		
		int m = (l + r) >>> 1;
		update(l, m, ul, ur, i * 2 + 1, val);
		update(m + 1, r, ul, ur, i * 2 + 2, val);
		seg[i] = combineQuery(seg[i * 2 + 1], seg[i * 2 + 2]);
	}
}

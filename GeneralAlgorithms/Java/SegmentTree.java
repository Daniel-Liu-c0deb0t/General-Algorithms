import java.util.Random;

public class SegmentTree{
	int n;
	int[] seg;
	
	public static void main(String[] args){
		int iter = 100000;
		SegmentTree st = new SegmentTree(iter);
		Random r = new Random();
		for(int i = 0; i < iter; i++)
			st.update(0, iter - 1, i, 0, i % 2 == 0 ? r.nextInt(5000) : 5000 + r.nextInt(5000));
		for(int i = 0; i < iter; i++)
			st.query(0, iter - 1, 0, i, 0);
		System.out.println(st.query(0, iter - 1, 0, iter, 0));
		
		SegmentTree st2 = new SegmentTree(5);
		st2.update(0, 5 - 1, 1, 0, 3);
		st2.update(0, 5 - 1, 2, 0, 2);
		System.out.println(st2.query(0, 5 - 1, 0, 2, 0));
	}
	
	SegmentTree(int n){
		this.n = n;
		this.seg = new int[n * 4];
	}
	
	int emptyQuery = 0;
	
	int combineQuery(int a, int b){
		return a + b;
	}
	
	int combineUpdate(int o, int val){
		return o + val;
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
	
	int construct(int l, int r, int i, int val){
		if(l == r){
			seg[i] = val;
			return seg[i];
		}
		int m = (l + r) >>> 1;
		seg[i] = combineQuery(construct(l, m, i * 2 + 1, val), construct(m + 1, r, i * 2 + 2, val));
		return seg[i];
	}
	
	int query(int l, int r, int ql, int qr, int i){
		if(l >= ql && qr >= r){
			return seg[i];
		}
		if(r < ql || l > qr){
			return emptyQuery;
		}
		int m = (l + r) >>> 1;
		return combineQuery(query(l, m, ql, qr, i * 2 + 1), query(m + 1, r, ql, qr, i * 2 + 2));
	}
	
	void update(int l, int r, int ui, int i, int val){
		if(r < ui || l > ui){
			return;
		}
		if(l == r){
			seg[i] = combineUpdate(seg[i], val);
			return;
		}
		int m = (l + r) >>> 1;
		update(l, m, ui, i * 2 + 1, val);
		update(m + 1, r, ui, i * 2 + 2, val);
		seg[i] = combineQuery(seg[i * 2 + 1], seg[i * 2 + 2]);
	}
}

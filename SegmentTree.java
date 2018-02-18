
public class SegmentTree{
	int n;
	int[] seg;
	
	public static void main(String[] args){
		int[] arr = {1, 2, 3, 4, 5};
		SegmentTree st = new SegmentTree(arr.length);
		st.construct(arr, 0, arr.length - 1, 0);
		st.update(0, arr.length - 1, 1, 0, 3);
		System.out.println(st.query(0, arr.length - 1, 0, 1, 0));
	}
	
	SegmentTree(int n){
		this.n = n;
		this.seg = new int[n * 4 + 1];
	}
	
	int construct(int[] arr, int l, int r, int i){
		if(l == r){
			seg[i] = arr[l];
			return seg[i];
		}
		int m = l + (r - l) / 2;
		seg[i] = construct(arr, l, m, i * 2 + 1) + construct(arr, m + 1, r, i * 2 + 2);
		return seg[i];
	}
	
	int query(int l, int r, int ql, int qr, int i){
		if(l >= ql && qr >= r){
			return seg[i];
		}
		if(r < ql || l > qr){
			return 0;
		}
		int m = l + (r - l) / 2;
		return query(l, m, ql, qr, i * 2 + 1) + query(m + 1, r, ql, qr, i * 2 + 2);
	}
	
	void update(int l, int r, int ui, int i, int val){
		if(r < ui || l > ui){
			return;
		}
		if(l == r){
			seg[i] += val;
		}else{
			int m = l + (r - l) / 2;
			update(l, m, ui, i * 2 + 1, val);
			update(m + 1, r, ui, i * 2 + 2, val);
			seg[i] = seg[i * 2 + 1] + seg[i * 2 + 2];
		}
	}
}

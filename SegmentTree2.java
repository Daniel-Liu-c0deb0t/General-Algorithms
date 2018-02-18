
public class SegmentTree2{
	int n;
	int[] seg;
	int[] lazy;
	
	public static void main(String[] args){
		int[] arr = {1, 2, 3, 4, 5};
		SegmentTree2 st = new SegmentTree2(arr.length);
		st.construct(arr, 0, arr.length - 1, 0);
		st.update(0, arr.length - 1, 1, 2, 0, 3);
		System.out.println(st.query(0, arr.length - 1, 0, 2, 0));
	}
	
	SegmentTree2(int n){
		this.n = n;
		seg = new int[n * 4 + 1];
		lazy = new int[n * 4 + 1];
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
		if(lazy[i] != 0){
			if(l != r){
				lazy[i * 2 + 1] += lazy[i];
				lazy[i * 2 + 2] += lazy[i];
			}
			seg[i] += (r - l + 1) * lazy[i];
			lazy[i] = 0;
		}
		if(r < ql || l > qr){
			return 0;
		}
		if(l >= ql && qr >= r){
			return seg[i];
		}
		int m = l + (r - l) / 2;
		return query(l, m, ql, qr, i * 2 + 1) + query(m + 1, r, ql, qr, i * 2 + 2);
	}
	
	void update(int l, int r, int ul, int ur, int i, int val){
		if(lazy[i] != 0){
			if(l != r){
				lazy[i * 2 + 1] += lazy[i];
				lazy[i * 2 + 2] += lazy[i];
			}
			seg[i] += (r - l + 1) * lazy[i];
			lazy[i] = 0;
		}
		if(r < ul || l > ur){
			return;
		}
		if(l >= ul && r <= ur){
			seg[i] += (r - l + 1) * val;
			if(l != r){
				lazy[i * 2 + 1] += val;
				lazy[i * 2 + 2] += val;
			}
		}else{
			int m = l + (r - l) / 2;
			update(l, m, ul, ur, i * 2 + 1, val);
			update(m + 1, r, ul, ur, i * 2 + 2, val);
			seg[i] = seg[i * 2 + 1] + seg[i * 2 + 2];
		}
	}
}

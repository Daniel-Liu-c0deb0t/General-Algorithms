
public class BinarySearch{
	public static void main(String[] args){
		int[] arr = {1, 3, 5, 5, 7, 9};
		//no negative numbers in arr!
		System.out.println(bSearch(arr, 5, false));
		System.out.println(bSearchLower(arr, 10));
		System.out.println(bSearch(arr, 8, true));
		System.out.println(bSearchHigher(arr, 8));
		System.out.println(bSearchSqrt(2));
		System.out.println(bSearchSqrt(1234567));
	}
	
	static int bSearch(int[] arr, int t, boolean upper){
		int l = 0, r = arr.length - 1, res = -1;
		while(l <= r){
			int m = (l + r) >>> 1;
			if(arr[m] > t){
				r = m - 1;
			}else if(arr[m] < t){
				l = m + 1;
			}else{
				res = m;
				if(upper){
					l = m + 1;
				}else{
					r = m - 1;
				}
			}
		}
		return res;
	}
	
	static int bSearchLower(int[] arr, int t){
		int l = 0, r = arr.length - 1;
		while(l < r){
			int m = (l + r + 1) >>> 1;
			if(arr[m] > t){
				r = m - 1;
			}else{
				l = m;
			}
		}
		return l;
	}
	
	static int bSearchHigher(int[] arr, int t){
		int l = 0, r = arr.length - 1;
		while(l < r){
			int m = (l + r - 1) >>> 1;
			if(arr[m] < t){
				l = m + 1;
			}else{
				r = m;
			}
		}
		return r;
	}
	
	//example of square rooting
	static double bSearchSqrt(double t){
		double l = 0.0, r = t, res = -1.0;
		while(Math.abs(r - l) > 1e-7){ //guaranteed 6 "good" digits
			double m = l + (r - l) / 2.0;
			if(m * m <= t){
				l = m;
				res = m;
			}else{
				r = m;
			}
		}
		return res;
	}
}
